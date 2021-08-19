
from app import app
from flask import request , jsonify
from flask.views import MethodView
from app.models import *
from datetime import datetime,date
from sqlalchemy import func
from werkzeug.exceptions import HTTPException
import uuid
import os 

UPLOAD_SHOP = './app/static/shop-pictures/'
UPLOAD_FOOD = './app/static/food-pictures/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_SHOP'] = UPLOAD_SHOP
app.config['UPLOAD_FOOD'] = UPLOAD_FOOD





@app.route("/")
def home():
    return jsonify({"hello":"words"})




class ShopPictures(MethodView):
    def get(self,filename):
        url = '/static/shop-pictures/' + filename
        return '<img src=' + url + '>'
    def post(self):
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(app.config['UPLOAD_SHOP'], f_name))
        link = request.base_url + '/' +  f_name
        return  {  "pictures_shop" :  link }
class FoodPictures(MethodView): 
    def get(self,filename):
        url = '/static/food-pictures/' + filename
        return '<img src=' + url + '>'
    def post(self):
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(app.config['UPLOAD_FOOD'], f_name))
        link = request.base_url + '/' +  f_name
        return  {  "pictures_food" :  link }



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
            shop_pictures = request.json['shop_pictures']
            shop = Shop(name = name , shop_pictures = shop_pictures , address = address , phone = phone)
            db.session.add(shop)
            db.session.commit()
            return self.shop_schema.jsonify(shop)
        else:
            shop = Shop.query.get(shop_id)
            name = request.json['name']
            price = request.json['price']
            food_pictures = request.json['food_pictures']
            food = Food(name = name ,food_pictures = food_pictures , price = price , shop = shop)
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
            shop.shop_pictures = request.json['shop_pictures']
            db.session.commit()
            return self.shop_schema.jsonify(shop)
        else:
            food = Food.query.get(food_id)
            food.name = request.json['name']
            food.price = request.json['price']
            food.food_pictures = request.json['food_pictures']     
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
            food_name = food.name
            shop = food.shop.name
            bill = Bill_detail(quantity = quantity , food = food ,daily_order = daily_order, food_name = food_name , shop = shop)
            result.append(bill)
            daily_order.total += quantity*food.price
        # if request.json["status"]  and request.json["status"] == True or request.json["status"] == False:
        #     if request.json["status"] == True:
        #         daily_order.completed = daily_order.total
        #     else:
        #         daily_order.pending = daily_order.total

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

class ConsolidationAPI(MethodView):
    consolidationSchema = Order_consolidationSchema()
    consolidations_Schema = Order_consolidationSchema(many = True)
    orders_schema = DailySchema(many=True)
    order_schema = DailySchema()
    bills_schema = BillSchema(many=True)
    def get(self,orders_id , order_id):
        if orders_id is None and order_id is None:
            consolidation = Order_consolidation.query.all()
            result = self.consolidations_Schema.dump(consolidation)
            print(result)
            return jsonify(result)
        elif orders_id != None and order_id == None:
            consolidation = Order_consolidation.query.get(orders_id)
            order = consolidation.daily_order
            orders = self.orders_schema.dump(order)
            result = self.consolidationSchema.dump(consolidation)
            result["orders"] = orders
            return jsonify(result)
        elif  orders_id != None and order_id != None:
            order = Daily_order.query.get(order_id)
            bill = order.bill
            daily_result = self.order_schema.dump(order)
            bill_result = self.bills_schema.dump(bill)
            daily_result["bill"] = bill_result
            return jsonify(daily_result)



    def post(self):
        consolidation = Order_consolidation(total = 0)
        foods = []
        list_food = {}
        foods_quantity = 0
        for i in request.json["bill_orders"]:
            order = Daily_order.query.get(i["id"])
            if order.canceled == False:
                consolidation.total += order.total
                order.confirm = True
                if i["status"] == True:
                    order.status = True
                    order.completed = order.total
                    order.pending = 0
                elif i["status"] == False:
                    order.status = False
                    order.pending = order.total
                    order.completed = 0
                order.order_consolidation = consolidation
                for j in order.bill:
                    if j.food_id not in  foods:
                        foods.append(j.food_id)
                        list_food[j.food_id] ={"name" : j.food_name ,"quantity": j.quantity}
                    else:
                        list_food[j.food_id]["quantity"] += j.quantity
            elif order.canceled == True:
                order.total = 0
            
        for key,value in list_food.items():
            foods_quantity += value["quantity"]
            
            
        db.session.add(consolidation)
        db.session.commit()
        result = self.consolidationSchema.dump(consolidation)
        print(result)
        add = {"foods_quantity" : foods_quantity , "list_food" : list_food }
        result.update(add)
        return jsonify(result)
        

@app.route('/admin/statistical/today' , methods = ['GET'])
def statistical_thisday():
    daily = db.session.query(Daily_order).filter(func.DATE(Daily_order.date) == date.today())
    foods = []
    list_food = {}
    total = 0
    sum = 0
    for i in daily:
        if i.canceled == False:
            for j in i.bill:
                if j.food_id not in  foods:
                    foods.append(j.food_id)
                    list_food[j.food_id] ={"name" : j.food_name ,"quantity": j.quantity}
                else:
                    list_food[j.food_id]["quantity"] += j.quantity
    for key,value in list_food.items():
        sum += value["quantity"]
        total += Food.query.get(key).price * value["quantity"]
    result = {"sum": sum , "total": total  , "foods": list_food }
    return jsonify(result)             

    
#User xem thống kê theo tháng
@app.route('/statistical/month' , methods = ['GET'])

def User_statistical():
    user_email = request.json['user_email']
    daily = Daily_order.query.filter_by(user_email = user_email).all()
    pending = 0
    completed = 0
    count = 0
    canceled = 0
    for i in daily:
        if i.date.month == date.today().month:
            if i.canceled != True and i.confirm == True:
                pending += i.pending
                completed += i.completed
                count +=1
            else:
                canceled +=1
    return jsonify({'order_completed': count,'completed':completed,'pending':pending , "order_canceled":canceled})

#admin xem tất cả order hôm nay
@app.route('/admin/daily_order/' , methods = ['GET'])
def daily_order():
    dailys_schema = DailySchema(many = True)
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
@app.route('/admin/repair_bill/<int:order_id>' , methods = ['PUT'])
def repair_bill(order_id):
    order_schema = DailySchema()
    order = Daily_order.query.get(order_id)
    a = order.status
    order.status = request.json['status']    
    if a != order.status:
        if order.status == True:
            order.pending = 0
            order.completed = order.total
        else:
            order.pending = order.total
            order.completed = 0
    db.session.commit()
    return order_schema.jsonify(order)

@app.route('/history/canceled/' , methods = ['GET'])
def canceled():
    order_schema = DailySchema(many = True)
    user = request.json["user_email"]
    order = Daily_order.query.filter_by(user_email = user , canceled = True).all()
    result = order_schema.dump(order)
    return jsonify(result)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

#Shop & Food 

#Shop pictures
shop_pictures = ShopPictures.as_view('shop_pictures')
app.add_url_rule('/uploadShop/' , view_func= shop_pictures , methods = ['POST'])
app.add_url_rule('/uploadShop/<filename>' , view_func= shop_pictures , methods = ['GET'])


#Food pictures
food_pictures = FoodPictures.as_view('food_pictures')
app.add_url_rule('/uploadFood/' , view_func= food_pictures , methods = ['POST'])
app.add_url_rule('/uploadFood/<filename>' , view_func= food_pictures , methods = ['GET'])

#Shop & food api
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

#admin consolidation order
confirm = ConsolidationAPI.as_view('confirm')
app.add_url_rule('/confirm/' ,defaults = {'orders_id':None,'order_id':None}, view_func= confirm , methods = ['POST','GET'])
app.add_url_rule('/confirm/<orders_id>' , defaults = {'order_id':None},view_func= confirm , methods = ['GET'])
app.add_url_rule('/confirm/<orders_id>/order/<order_id>' , view_func= confirm , methods = ['GET'])