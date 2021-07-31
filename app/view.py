
from app import app
from flask import request , jsonify
from flask.views import MethodView
from app.models import *
from datetime import datetime,date
from sqlalchemy import func

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
            daily_result["bill"] = bill_result
            return jsonify(daily_result)
        else:
            bill  = Bill_detail.query.get(bill_id)
            return self.bill_schema.jsonify(bill)



        
    def post(self):
        user_email = request.json['user_email']
        daily_order = Daily_order(user_email = user_email , pending = 0 ,completed = 0, total = 0)
        result = []
        for json in request.json["order"]:
            food_id =  json['food_id']
            food = Food.query.get(food_id)
            quantity = json['quantity']
            status = json['status']
            food_name = food.name
            shop = food.shop.name
            bill = Bill_detail(quantity = quantity , status = status , food = food ,daily_order = daily_order, food_name = food_name , shop = shop)
            result.append(bill)
            if status == True:
                daily_order.completed += quantity*food.price
                daily_order.total += quantity*food.price
            else:
                daily_order.pending += quantity*food.price
                daily_order.total += quantity*food.price
            
        db.session.add(daily_order)
        db.session.commit()
        result = self.bills_schema.dump(result)
        daily_order = self.daily_schema.dump(daily_order)
        daily_order["bills"] = result
        return jsonify(daily_order)
    def put(self,order_id):
        order = Daily_order.query.get(order_id)
        order.canceled = request.json["canceled"]
        if order.canceled:
            order.total = 0
            order.completed = 0
            order.pending = 0
        db.session.commit()
        return self.daily_schema.jsonify(order)

@app.route('/test' , methods = ["GET"])
def test():
    data = request.json
    
    print(type(data))
    return("done")

#Thống kê theo tháng
@app.route('/statistical' , methods = ['GET'])

def User_statistical():
    user_email = request.json['user_email']
    daily = Daily_order.query.filter_by(user_email = user_email).all()
    pending = 0
    completed = 0
    count = 0
    canceled = 0
    for i in daily:
        if i.date.month == date.today().month:
            if i.canceled != True:
                pending += i.pending
                completed += i.completed
                count +=1
            else:
                canceled +=1
    return jsonify({'count': count,'completed':completed,'pending':pending , "canceled":canceled})
#admin xem tất cả order hôm nay
@app.route('/admin/daily_order/' , methods = ['GET'])
def daily_order():
    dailys_schema = DailySchema(many = True)
    # daily = Daily_order.query.filter(Daily_order.date.today() == date.today()).all()
    daily = db.session.query(Daily_order).filter(func.DATE(Daily_order.date) == date.today())
    result = dailys_schema.dump(daily)
    return jsonify(result)
#admin xem tất cả order
@app.route('/admin/all_order/' , methods = ['GET'])
def all_order():
    dailys_schema = DailySchema(many = True)
    daily = Daily_order.query.all()
    result = dailys_schema.dump(daily)
    return jsonify(result)
#admin sửa trạng thái món ăn đã/chưa thanh toán
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

@app.route('/history/canceled/' , methods = ['GET'])
def canceled():
    order_schema = DailySchema(many = True)
    user = request.json["user_email"]
    order = Daily_order.query.filter_by(user_email = user , canceled = True).all()
    result = order_schema.dump(order)
    return jsonify(result)





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
app.add_url_rule('/order/<int:order_id>'  , view_func= order_view , methods = ['PUT'])
app.add_url_rule('/history/' , defaults = {'order_id':None ,'bill_id':None}, view_func= order_view , methods = ['GET'])
app.add_url_rule('/history/<int:order_id>' , defaults = {'bill_id':None}, view_func= order_view , methods = ['GET'])
app.add_url_rule('/history/<int:order_id>/bill/<int:bill_id>'  , view_func= order_view , methods = ['GET'])

# app.add_url_rule('/<user_email>/canceled/<int:bill_id>'  , view_func= order_view , methods = ['PUT'])