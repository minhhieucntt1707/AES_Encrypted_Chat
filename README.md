# AES_Encrypted_Chat
# Ứng Dụng Nhắn Tin An Toàn - AES Encrypted Chat

Đây là một ứng dụng nhắn tin cơ bản trên web sử dụng mã hóa AES (Advanced Encryption Standard) để đảm bảo tính bảo mật cho các tin nhắn giữa người dùng.

## Tính năng chính

- Giao diện web đơn giản, dễ sử dụng.
- Gửi và nhận tin nhắn theo thời gian thực (sử dụng WebSocket hoặc polling).
- Tất cả tin nhắn đều được mã hóa bằng AES trước khi gửi.
- Mỗi người dùng có một khóa mã hóa riêng hoặc chia sẻ khóa chung trong phiên (tuỳ thiết kế).
- Tin nhắn được giải mã chỉ khi đến người nhận.

## Công nghệ và thư viện sử dụng

- **Frontend**: HTML, Bootstrap, JavaScript, CryptoJS
- **Backend**: Python, Flask, Flask-SocketIO
- **Giao tiếp thời gian thực**: WebSocket (qua Socket.IO)
- **Mã hóa**: AES-CBC với khóa dẫn xuất từ PBKDF2 (CryptoJS)

## Cách Ứng Dụng Bảo Mật Tin Nhắn

-Tin nhắn được mã hóa ngay trên trình duyệt của người gửi bằng AES-CBC.
-Khóa AES được dẫn xuất từ mật khẩu bằng thuật toán PBKDF2, sử dụng salt cố định và 1000 vòng lặp.
-Người nhận cần nhập đúng khóa AES để giải mã tin nhắn.
-Máy chủ không biết và không lưu trữ khóa AES — chỉ truyền tin nhắn đã mã hóa.

## Các Tính Năng Chính

-**Mã hóa AES client-side:** không gửi bản rõ lên server.
-Nhắn tin riêng tư 1-1 giữa các người dùng đang online.
-Lưu lịch sử hội thoại (đã mã hóa) trên server.
-Xác thực khóa AES bằng cách giải mã thử tin nhắn đầu tiên.
-Danh sách người dùng online được cập nhật theo thời gian thực.
-Tự động hiển thị tin nhắn đã nhận nếu đã có khóa đúng.

## Giao Diện Người Dùng
-**Trang chủ (temp_index.html):** giới thiệu ứng dụng.
Giao diện chat:
  Login bằng tên người dùng.
  Chọn người để nhắn tin.
  Nhập khóa AES để kích hoạt trò chuyện.
  Gửi và nhận tin nhắn được mã hóa.

##  Ghi Chú Quan Trọng
Mã hóa sử dụng iv ngẫu nhiên cho mỗi tin nhắn (đảm bảo bảo mật).
Trên môi trường thực tế:
  Nên có cơ chế trao đổi khóa an toàn (VD: Diffie-Hellman).
  Sử dụng HTTPS để tránh tấn công MITM.
