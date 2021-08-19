
from app import db , ma 
from datetime import datetime,date
from sqlalchemy.sql.expression import Executable, ClauseElement



class Shop(db.Model):
    __tablename__  = "shop"
    id =  db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(120) ,index = True)
    shop_pictures =  db.Column(db.String(120) ,index = True)
    address = db.Column(db.String(120) ,index = True)
    phone = db.Column(db.Integer ,index = True)
    food = db.relationship('Food', backref='shop', cascade="all, delete")
    
class ShopSchema(ma.Schema):
    class Meta:
        fields = ("id" ,"name" ,"shop_pictures", "address" , "phone" )




class Food(db.Model):
    __tablename__  = "food"
    id =  db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(120) ,index = True)
    food_pictures = db.Column(db.String(120) ,index = True)
    price = db.Column(db.Integer , index = True)
    shop_id = db.Column(db.Integer , db.ForeignKey('shop.id'))
    bill = db.relationship('Bill_detail', backref='food')
 
class FoodSchema(ma.Schema):
    class Meta:
        fields = ("id" ,"name" ,"food_pictures" , "price","shop_id")




class Bill_detail(db.Model):
    __tablename__  = "bill_detail"
    id =  db.Column(db.Integer,primary_key = True)
    quantity = db.Column(db.Integer ,index = True)
    food_id = db.Column(db.Integer , db.ForeignKey('food.id'))
    order = db.Column(db.Integer , db.ForeignKey('daily_order.id'))
    food_name = db.Column(db.String(120),index = True)
    shop = db.Column(db.String(120),index = True)

class BillSchema(ma.Schema):
    class Meta:
        fields = ("id" ,"quantity"  ,"food_id","order","food_name","shop")





class Daily_order(db.Model):
    __tablename__  = "daily_order"
    id = db.Column(db.Integer , primary_key = True)
    user_email = db.Column(db.String(120), index = True)
    date = db.Column(db.DateTime, index=True, default=datetime.now)
    pending  = db.Column(db.Integer , index = True )
    completed = db.Column(db.Integer , index = True)
    bill = db.relationship('Bill_detail', backref='daily_order' , cascade="all, delete")
    total = db.Column(db.Integer ,index = True)
    canceled = db.Column(db.Boolean, default=False, nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)
    confirm = db.Column(db.Boolean, default=False, nullable=False)
    consolidation = db.Column(db.Integer , db.ForeignKey('order_consolidation.id'))

class DailySchema(ma.Schema):
    class Meta:
        fields = ("id" ,"user_email" , "date" , "pending","completed" ,"canceled","total" , "confirm" ,"status" ,"confirm" , "consolidation")  
        


class Order_consolidation(db.Model):
    __tablename__  = "order_consolidation"
    id = db.Column(db.Integer , primary_key = True)
    date = db.Column(db.DateTime, index=True, default=datetime.now)
    total = db.Column(db.Integer ,index = True)
    daily_order = db.relationship('Daily_order', backref='order_consolidation' , cascade="all, delete")

class Order_consolidationSchema(ma.Schema):
    class Meta:
        fields = ("id" ,"date" ,"total")






















