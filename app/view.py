from os import name
from sqlalchemy import schema
from app import app
from flask import request , jsonify
from flask.views import MethodView
from app.models import *
from datetime import datetime,date


@app.route("/")
def home():
    return jsonify({"hello":"words"})

class ShopAPI(MethodView):
    shop_schema = ShopSchema()
    shops_schema = ShopSchema(many=True)
    food_schema = FoodSchema()
    foods_schema = FoodSchema(many=True)

    def get(self, shop_id,food_id):
        if shop_id is None:
            # return a list of shops
            shop = Shop.query.all()
            print(shop)
            result = self.shops_schema.dump(shop)
            return jsonify(result)
        else:
            # expose a single shop
            if food_id is None:
                shop = Shop.query.get(shop_id)
                print(shop)
                food = shop.food
                shop_result = self.shop_schema.dump(shop)
                food_result = self.foods_schema.dump(food)
                shop_result["food"] = food_result
                return jsonify(shop_result)
            else:
                food = Food.query.get(food_id)
                if food.shop.id == shop_id:
                    return self.food_schema.jsonify(food)
                else:
                    return "Món ăn không thuộc shop bạn đang chỉ định"


    def post(self,shop_id):
        # create a new shop
        if shop_id is None:
            name = request.json['name']
            address = request.json['address']
            phone = request.json['phone']
            shop = Shop(name = name , address = address , phone = phone)
            db.session.add(shop)
            db.session.commit()
            return self.shop_schema.jsonify(shop)
        else:
            shop = Shop.query.get(shop_id)
            name = request.json['name']
            price = request.json['price']

            food = Food(name = name , price = price , shop = shop)
            db.session.commit()
            return self.food_schema.jsonify(food)


    def delete(self, shop_id , food_id):
        if food_id is None:
            shop = Shop.query.get(shop_id)
            db.session.delete(shop)
            db.session.commit()
            return self.shop_schema.jsonify(shop)
        else:
            food = Food.query.get(food_id)
            db.session.delete(food)
            db.session.commit()
            return self.food_schema.jsonify(food)


    def put(self, shop_id, food_id):
        # update a single shop
        if food_id is None:
            shop = Shop.query.get(shop_id)
            shop.name = request.json['name']
            shop.address = request.json['address']
            shop.phone = request.json['phone']
            db.session.commit()
            return self.shop_schema.jsonify(shop)
        else:
            food = Food.query.get(food_id)
            food.name = request.json['name']
            food.price = request.json['price']     
            db.session.commit()
            return self.food_schema.jsonify(food)





class OrderApi(MethodView):
    bill_schema = BillSchema()
    bills_schema = BillSchema(many=True)
    daily_schema = DailySchema()
    dailys_schema = DailySchema(many= True) 
    
    def get(self,order_id , bill_id ):
        user_email = request.json['user_email']
        if order_id is None and bill_id is None :
            daily_order = Daily_order.query.filter_by(user_email = user_email).all()
            print(daily_order)
            result = self.dailys_schema.dump(daily_order)
            return jsonify(result)
        elif order_id and bill_id is None:
            daily_order = Daily_order.query.get(order_id)
            print(daily_order.date.month)
            bill = daily_order.bill
            daily_result = self.daily_schema.dump(daily_order)
            bill_result = self.bills_schema.dump(bill)
            for i in bill_result:
                i["total"] = Food.query.get(i["food_id"]).price*i["quantity"]
                i["food_name"] = Food.query.get(i["food_id"]).name
                i["shop"] = Food.query.get(i["food_id"]).shop.name
            daily_result["bill"] = bill_result
            return jsonify(daily_result)
        else:
            bill  = Bill_detail.query.get(1)
            return self.bill_schema.jsonify(bill)



        
    def post(self):
        user_email = request.json['user_email']
        order =  Daily_order.query.filter_by(user_email = user_email , date = date.today()).first()
        print(order)
        if order:
            food_id =  request.json['food_id']
            food = Food.query.get(food_id)
            quantity = request.json['quantity']
            status = request.json['status']
            bill = Bill_detail(quantity = quantity , status = status , food = food ,daily_order = order)
            if status == True:
                order.completed += quantity*food.price
            else:
                order.pending += quantity*food.price
            db.session.commit()
            bill = self.bill_schema.dump(bill)
            bill["total"] = quantity*food.price
            bill["food_name"] = food.name
            bill["shop"] = food.shop.name
            return jsonify(bill)
        else:
            daily_order = Daily_order(user_email = user_email , pending = 0 ,completed = 0)
            food_id =  request.json['food_id']
            food = Food.query.get(food_id)
            quantity = request.json['quantity']
            status = request.json['status']
            bill = Bill_detail(quantity = quantity , status = status , food = food ,daily_order = daily_order)
            if status == True:
                daily_order.completed += quantity*food.price
            else:
                daily_order.pending += quantity*food.price
            db.session.add(daily_order)
            db.session.commit()
            bill = self.bill_schema.dump(bill)
            bill["total"] = quantity*food.price
            bill["food_name"] = food.name
            bill["shop"] = food.shop.name
            return jsonify(bill)
    def put(self,bill_id):
        bill = Bill_detail.query.get(bill_id)
        bill.canceled = True
        food_id = bill.food_id
        food = Food.query.get(food_id)
        if bill.status == True:
            bill.daily_order.completed -= bill.quantity*food.price
        else:
            bill.daily_order.pending -= bill.quantity*food.price
        db.session.commit()
        bill = self.bill_schema.dump(bill)
        bill["total"] = bill.quantity*food.price
        bill["food_name"] = food.name
        bill["shop"] = food.shop.name
        return jsonify(bill)



#Thống kê theo tháng
@app.route('/statistical' , methods = ['GET'])

def User_statistical():
    user_email = request.json['user_email']
    daily = Daily_order.query.filter_by(user_email = user_email).all()
    pending = 0
    completed = 0
    count = 0
    for i in daily:
        if i.date.month == date.today().month:
            pending += i.pending
            completed += i.completed
            count +=1
    return jsonify({'count': count,'completed':completed,'pending':pending})
    
@app.route('/admin/daily_order/' , methods = ['GET'])
def daily_order():
    dailys_schema = DailySchema(many = True)
    daily = Daily_order.query.filter_by(date = date.today()).all()
    result = dailys_schema.dump(daily)
    return jsonify(result)

@app.route('/admin/all_order/' , methods = ['GET'])
def all_order():
    dailys_schema = DailySchema(many = True)
    daily = Daily_order.query.all()
    result = dailys_schema.dump(daily)
    return jsonify(result)
@app.route('/admin/repair_bill/<int:bill_id>' , methods = ['PUT'])
def repair_bill(bill_id):
    bill_schema = BillSchema()
    bill = Bill_detail.query.get(bill_id)
    a = bill.status
    bill.status = request.json['status']  
    food_id = bill.food_id
    food = Food.query.get(food_id)
    if a != bill.status:
        if bill.status == True:
            bill.daily_order.pending -= bill.quantity*food.price
            bill.daily_order.completed += bill.quantity*food.price
        else:
            bill.daily_order.completed -= bill.quantity*food.price
            bill.daily_order.pending += bill.quantity*food.price
    db.session.commit()
    return bill_schema.jsonify(bill)



# @app.route('/<user_email>/canceled' , methods = ['GET'])
# def User_canceled(user_email):
#     bills_schema = BillSchema(many =True)
#     order = Daily_order.query.filter_by(user_email = user_email).all()
#     result = []
#     for i in order:
#         for j in i.bill:
#             if j.canceled == True:
#                 result.append(j)
#     kq = bills_schema.dump(result)
#     return jsonify(kq)



#Shop & Food 

shop_view = ShopAPI.as_view('shop_api')
app.add_url_rule('/shop/' , defaults = {'shop_id':None,'food_id':None} , view_func= shop_view , methods = ['GET'])
app.add_url_rule('/shop/' , defaults = {'shop_id':None} ,view_func= shop_view , methods = ['POST'])
app.add_url_rule('/shop/<int:shop_id>' ,defaults = {'food_id':None} , view_func= shop_view , methods = ['GET','PUT','DELETE'])
app.add_url_rule('/shop/<int:shop_id>/food/' , view_func= shop_view , methods = ['POST'])
app.add_url_rule('/shop/<int:shop_id>/food/<int:food_id>' , view_func= shop_view , methods = ['GET','PUT','DELETE'])

#user order & history
order_view = OrderApi.as_view("order_api")
app.add_url_rule('/order'  , view_func= order_view , methods = ['POST'])
app.add_url_rule('/order/<int:bill_id>'  , view_func= order_view , methods = ['PUT'])
app.add_url_rule('/history/' , defaults = {'order_id':None ,'bill_id':None}, view_func= order_view , methods = ['GET'])
app.add_url_rule('/history/<int:order_id>' , defaults = {'bill_id':None}, view_func= order_view , methods = ['GET'])
app.add_url_rule('/history/<int:order_id>/bill/<int:bill_id>'  , view_func= order_view , methods = ['GET'])

# app.add_url_rule('/<user_email>/canceled/<int:bill_id>'  , view_func= order_view , methods = ['PUT'])