# flaskApi

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
