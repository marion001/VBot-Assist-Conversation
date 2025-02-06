## Tích Hợp Trợ Lý Ảo Loa Thông Minh VBot Assistant Vào Assist (Tác Nhân) trong Home Assistant

## Cài Đặt
1. Cài đặt [bằng cách đăng ký làm kho lưu trữ tùy chỉnh của HACS thêm trực tiếp url]
     - đi tới HACS -> Kho lưu trữ tùy chỉnh ->Thêm URL: https://github.com/marion001/VBot-Assist-Conversation.git -> chọn Kiểu là: "Bộ Tích Hợp" -> nhấn "Thêm"
  
       
2. Hoặc Cài Đặt Thủ Công:
    - bằng cách tải về và sao chép toàn bộ thư mục `vbot_assist` vào trong thư mục `custom_components` của bạn cấu trúc thư mục sẽ là:  `custom_components/vbot_assist`
  
      
3. Khởi động lại Home Assistant
4. Đi tới: Cài đặt > Thiết bị & Dịch vụ
5. Ở góc dưới cùng bên phải, chọn nút Thêm tích hợp -> tìm kiếm với tên: "VBot Assistant"
6. Làm theo hướng dẫn trên màn hình để hoàn tất thiết lập (cần nhập URL API của VBot: Ví Dụ: http://192.168.14.113:5002)
7. Nếu cấu hình thành công Loa VBot sẽ phát 1 thông báo lời chào 
8. Vào Cài đặt > [Trợ lý giọng nói]
9. Nhấp để chỉnh sửa Trợ lý (chọn nhân viên hội thoại là: "VBot Assistant") và chọn làm mặc định (Đặt làm ưu tiên)
10. Sau khi hoàn tất các bước bạn có thể nhập dữ liệu để kiểm tra như: "mấy giờ rồi"

![Image](https://github.com/user-attachments/assets/c7a58d0e-dc57-41a1-afa1-f5f9d82b9014)


![Image](https://github.com/user-attachments/assets/d449b5b5-e5bb-42ed-9a36-6749d8e9a58a)


![Image](https://github.com/user-attachments/assets/ef877d6d-d8e2-4a7b-94aa-11077683c4ba)
