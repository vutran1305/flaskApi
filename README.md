# flaskApi

#Shop & Food 


- '/shop/' ,  methods = ['GET'] : Xem thông tin tất cả các shop
*Kết quả ví dụ:

![image](https://user-images.githubusercontent.com/72801957/127481254-e0315d63-d151-4f0a-9968-7defe08ed0dc.png)

- '/shop/' ,  methods = ['POST'])
- '/shop/<int:shop_id>' , methods = ['GET','PUT','DELETE']
- '/shop/<int:shop_id>/food/'  , methods = ['POST']
- '/shop/<int:shop_id>/food/<int:food_id>' , methods = ['GET','PUT','DELETE']

#user order & history

- '/order'  , methods = ['POST']
- '/order/<int:bill_id>'  , methods = ['PUT']
- '/history/'  , methods = ['GET']
- '/history/<int:order_id>' , methods = ['GET']
- '/history/<int:order_id>/bill/<int:bill_id>'  , methods = ['GET']

- '/statistical' , methods = ['GET']
- '/admin/daily_order/' , methods = ['GET']
- '/admin/all_order/' , methods = ['GET']
- '/admin/repair_bill/<int:bill_id>' , methods = ['PUT']
