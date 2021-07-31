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
### '/shop/<int:shop_id>/food/'  , methods = ['POST'] : Thêm món ăn mới vào shop
- Ví dụ
- ![image](https://user-images.githubusercontent.com/72801957/127483822-1bee8697-0130-4952-b2fe-a04364c4ffbb.png)

### '/shop/<int:shop_id>/food/<int:food_id>' , methods = ['GET','PUT','DELETE'] : Xem sửa xóa món ăn của shop
- VD methods = PUT
- ![image](https://user-images.githubusercontent.com/72801957/127484127-09dde1d8-72bb-4c97-aaad-544e9827ccf1.png)

## user order & history

### '/order'  , methods = ['POST'] : Đặt món ăn 
- Ví dụ đặt 1 món ăn :
- ![image](https://user-images.githubusercontent.com/72801957/127623577-d0d44ae0-464f-4754-a765-f758e13915cf.png)
- Ví dụ đặt 2 món ăn khác nhau:
- ![image](https://user-images.githubusercontent.com/72801957/127749397-59038eea-7c3c-412e-b2ec-34379d749b39.png)
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

### '/statistical' , methods = ['GET']: Thống kê đặt hàng trong tháng
![image](https://user-images.githubusercontent.com/72801957/127749644-56fe63d7-42f5-4e99-8e5a-d6cfeb7c282f.png)
- Trong đó :
- canceled : số đơn hàng bị hủy
- completed : Số tiền đã hoàn thành
- pending : Số tiền còn đang thiếu
- count : số đơn hàng đã hoàn thành
### '/admin/daily_order/' , methods = ['GET'] :  Xem tất cả đơn hàng các user đặt trong ngày hôm nay
### '/admin/all_order/' , methods = ['GET'] : Xem tất cả đơn hàng
### '/admin/repair_bill/<int:bill_id>' , methods = ['PUT'] : Sửa trạng thái bill ( chưa thanh toán - > đã thanh toán và ngc lại )
- ![image](https://user-images.githubusercontent.com/72801957/127749875-09a322d7-9481-4495-a252-1f5a188429a2.png)

