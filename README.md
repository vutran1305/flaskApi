# flaskApi
- Python 3.9.0
## package
- flask
- python-dotenvn
- SQLAlchemy
- marshmallow-sqlalchemy
- Flask-Migrate 
- flask_marshmallow
- flask-cors 


## API
## Shop
### '/uploadShop/ , moethods = POST : upload ảnh shop
### '/shop/' ,  methods = ['GET'] : Xem thông tin tất cả các shop
+ Kết quả ví dụ:

![image](https://user-images.githubusercontent.com/72801957/127481254-e0315d63-d151-4f0a-9968-7defe08ed0dc.png)

### '/shop/' ,  methods = ['POST']) : Thêm shop mới , gửi request là đến server là chuỗi json , nhận lại Response là thông tin shop
- Ví dụ :
- ![image](https://user-images.githubusercontent.com/72801957/130141556-7581e53f-f620-43f9-b623-437822b43f14.png)


### '/shop/<int:shop_id>' , methods = ['GET','PUT','DELETE'] : Xem sửa xóa shop ,kết quả trả về là thông tin shop đc chọn
- VD methods = PUT
- ![image](https://user-images.githubusercontent.com/72801957/127483110-7f6f3a22-7154-47f3-acc6-380f7b971ebe.png)
- VD methods = DELETE
- ![image](https://user-images.githubusercontent.com/72801957/127483291-5a27b156-31b9-4f72-9e3f-483d4e1499f5.png)
### '/shop/<int:shop_id>/food/'  , methods = ['POST'] : Thêm món ăn mới vào shop
- Ví dụ
- ![image](https://user-images.githubusercontent.com/72801957/130141667-20c44b19-bc6c-4ba6-8455-732f2ea80a29.png)


### '/shop/<int:shop_id>/food/<int:food_id>' , methods = ['GET','PUT','DELETE'] : Xem sửa xóa món ăn của shop
- VD methods = PUT
- request chuỗi json { "name" : tên shop , "address" : địa chỉ , "phone" : sđt , "shop_pictures" }


### '/order/'  , methods = ['POST'] : Đặt món ăn 
- ![image](https://user-images.githubusercontent.com/72801957/130142639-57228ea4-9286-4920-9037-2634b51ab990.png)

### '/order/<int:order_id>'  , methods = ['PUT'] : Hủy đơn hàng
- Ví dụ
- ![image](https://user-images.githubusercontent.com/72801957/127749425-a01987fb-0360-459e-97f7-b8bf4f322928.png)

### '/history/'  , methods = ['GET'] : Xem lịch sử đặt hàng
- Ví dụ:
- ![image](https://user-images.githubusercontent.com/72801957/127749459-1df53b19-04a9-4f6e-8604-16799aa0b2d3.png)

### '/history/<int:order_id>' , methods = ['GET'] : Xem thông tin đơn hàng
- ![image](https://user-images.githubusercontent.com/72801957/127749480-07d54be3-34b1-4601-bfbd-6d84bbc5bc80.png)

### '/history/<int:order_id>/bill/<int:bill_id>'  , methods = ['GET'] : Xem chi tiết từng bill
- ![image](https://user-images.githubusercontent.com/72801957/127749494-9563e9a9-54bf-4bb4-abc1-f90bb4bb218a.png)
### '/history/canceled/' , methods = ['GET'] :Xem tất cả các đơn hàng đã bị hủy
- ![image](https://user-images.githubusercontent.com/72801957/127750002-56ceef00-fb22-46ed-8319-c592fc4fa6f3.png)

### '/statistical' , methods = ['GET']: Thống kê đặt hàng trong tháng
![image](https://user-images.githubusercontent.com/72801957/127749644-56fe63d7-42f5-4e99-8e5a-d6cfeb7c282f.png)
- Trong đó :
- order_canceled : số đơn hàng bị hủy
- completed : Số tiền đã hoàn thành
- pending : Số tiền còn đang thiếu
- order_completed : số đơn hàng đã hoàn thành
### '/admin/daily_order/' , methods = ['GET'] :  Xem tất cả đơn hàng các user đặt trong ngày hôm nay
### '/admin/all_order/' , methods = ['GET'] : Xem tất cả đơn hàng
### '/admin/repair_bill/<int:order_id>' , methods = ['PUT'] : Sửa trạng thái bill ( chưa thanh toán - > đã thanh toán và ngc lại ))
### '/admin/statistical/today' , methods = ['GET'] : Xem thống kê danh sách và số lượng các món ăn đã đặt hôm nay

## Gộp đơn
### '/confirm/'  methods = ['POST','GET'] : Xem tất cả đơn gộp hoặc tạo 1 đơn gộp
- ![image](https://user-images.githubusercontent.com/72801957/130145111-ca51bec8-b5f2-437a-b369-107057b4793c.png)
### '/confirm/<orders_id>'  methods = ['GET'] : Xem từng đơn gộp
### '/confirm/<orders_id>/order/<order_id>'  methods = ['GET'] : Chi tiết từng order trong mỗi đơn gộp
### '/food/'  methods = ['GET']) : tất cả món ăn
### '/food/<food_id>'  methods = ['GET','DELETE','PUT']) : xem , sửa từng món
