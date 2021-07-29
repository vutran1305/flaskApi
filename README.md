# flaskApi

# Shop & Food 


### '/shop/' ,  methods = ['GET'] : Xem thông tin tất cả các shop
+ Kết quả ví dụ:

![image](https://user-images.githubusercontent.com/72801957/127481254-e0315d63-d151-4f0a-9968-7defe08ed0dc.png)

### '/shop/' ,  methods = ['POST']) : Thêm shop mới , gửi request là đến server là chuỗi json , nhận lại Response là thông tin shop
- Ví dụ :
![image](https://user-images.githubusercontent.com/72801957/127482018-e0d06fde-7c01-47e9-9284-3add0b6d10ca.png)

### '/shop/<int:shop_id>' , methods = ['GET','PUT','DELETE'] : Xem sửa xóa shop ,kết quả trả về là thông tin shop đc chọn
- VD methods = GET
- ![image](https://user-images.githubusercontent.com/72801957/127483193-1704766b-5295-4106-9157-7fecc822524a.png)
- VD methods = PUT
- ![image](https://user-images.githubusercontent.com/72801957/127483110-7f6f3a22-7154-47f3-acc6-380f7b971ebe.png)
- VD methods = DELETE
- ![image](https://user-images.githubusercontent.com/72801957/127483291-5a27b156-31b9-4f72-9e3f-483d4e1499f5.png)
### '/shop/<int:shop_id>/food/'  , methods = ['POST']
### '/shop/<int:shop_id>/food/<int:food_id>' , methods = ['GET','PUT','DELETE']

## user order & history

### '/order'  , methods = ['POST']
### '/order/<int:bill_id>'  , methods = ['PUT']
### '/history/'  , methods = ['GET']
### '/history/<int:order_id>' , methods = ['GET']
### '/history/<int:order_id>/bill/<int:bill_id>'  , methods = ['GET']

### '/statistical' , methods = ['GET']
### '/admin/daily_order/' , methods = ['GET']
### '/admin/all_order/' , methods = ['GET']
### '/admin/repair_bill/<int:bill_id>' , methods = ['PUT']
