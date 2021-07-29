# flaskApi

#Shop & Food 


'/shop/' ,  , methods = ['GET']
'/shop/' ,  methods = ['POST'])
'/shop/<int:shop_id>' , methods = ['GET','PUT','DELETE']
'/shop/<int:shop_id>/food/'  , methods = ['POST']
'/shop/<int:shop_id>/food/<int:food_id>' , methods = ['GET','PUT','DELETE']

#user order & history

'/order'  , methods = ['POST']
'/order/<int:bill_id>'  , methods = ['PUT']
'/history/'  , methods = ['GET']
'/history/<int:order_id>' , methods = ['GET']
'/history/<int:order_id>/bill/<int:bill_id>'  , methods = ['GET']
