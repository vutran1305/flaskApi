
from app import db , ma 
from datetime import datetime,date


class Daily_order(db.Model):
    __tablename__  = "daily_order"
    id = db.Column(db.Integer , primary_key = True)
    user_email = db.Column(db.String(120), index = True)
    date = db.Column(db.Date, index=True, default=date.today)
    pending  = db.Column(db.Integer , index = True )
    completed = db.Column(db.Integer , index = True)
    bill = db.relationship('Bill_detail', backref='daily_order' , cascade="all, delete")

   
class DailySchema(ma.Schema):
    class Meta:
        fields = ("id" ,"user_email" , "date" , "pending","completed")

class Food(db.Model):
    __tablename__  = "food"
    id =  db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(120) ,index = True)
    price = db.Column(db.Integer , index = True)
    shop_id = db.Column(db.Integer , db.ForeignKey('shop.id'))
    bill = db.relationship('Bill_detail', backref='food')

 
class FoodSchema(ma.Schema):
    class Meta:
        fields = ("id" ,"name" , "date" , "price","shop_id")

class Bill_detail(db.Model):
    __tablename__  = "bill_detail"
    id =  db.Column(db.Integer,primary_key = True)
    quantity = db.Column(db.Integer ,index = True)
    status = db.Column(db.Boolean, default=False, nullable=False)
    order_time = db.Column(db.DateTime, index=True, default=datetime.now)
    food_id = db.Column(db.Integer , db.ForeignKey('food.id'))
    order = db.Column(db.Integer , db.ForeignKey('daily_order.id'))
    canceled = db.Column(db.Boolean, default=False, nullable=False)
class BillSchema(ma.Schema):
    class Meta:
        fields = ("id" ,"quantity" , "status" , "order_time","food_id","order","canceled")

class Shop(db.Model):
    __tablename__  = "shop"
    id =  db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(120) ,index = True)
    address = db.Column(db.String(120) ,index = True)
    phone = db.Column(db.Integer ,index = True)
    food = db.relationship('Food', backref='shop', cascade="all, delete")
 
class ShopSchema(ma.Schema):
    class Meta:
        fields = ("id" ,"name" , "address" , "phone")