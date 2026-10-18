# Hệ thống đặt phòng homestay StayEasy (StayEasy Homestay)

Web application quản lý đặt phòng homestay và nghỉ dưỡng trải nghiệm thông minh:
- **Dành cho Khách hàng**: Đăng ký/đăng nhập thành viên, khám phá các căn homestay (Bungalow sân vườn, Nhà gỗ thông vintage, Gác áp mái ngắm hoàng hôn, Villa hồ bơi, Glamping lều trại cao cấp), đặt phòng trực tuyến kèm yêu cầu tiệc nướng BBQ / bếp tự nấu, theo dõi đơn đặt, quản lý hồ sơ thành viên và hóa đơn lưu trú.
- **Dành cho Quản trị viên (Chủ / Quản lý Homestay)**: Dashboard thống kê công suất căn & lượt đặt, quản lý các loại hình homestay, quản lý danh sách căn & tiện ích giá phòng, duyệt và cập nhật trạng thái đơn đặt homestay (Chờ xác nhận, Đã nhận phòng, Đã hoàn thành, Đã hủy), quản lý hồ sơ khách hàng và lịch sử lưu trú / hóa đơn.
- **Trợ lý StayEasy Homestay Assistant**: Hỗ trợ tư vấn thông tin các căn, dịch vụ tiệc nướng BBQ, bếp nấu, lửa trại và quy định nhận/trả phòng.

---

## Yêu cầu hệ thống

- Node.js 18+
- MySQL 8.x (hoặc Docker MySQL)
- (Tùy chọn) Python 3.10+ nếu sử dụng Chatbot StayEasy Homestay Assistant

---

## Cài đặt & Khởi chạy nhanh

### 1. Khởi tạo Database

Nếu sử dụng Docker MySQL (container `mysql-ktpm` trên cổng 3306):
```bash
docker exec -i mysql-ktpm mysql -u root -proot ttcsn < database.sql
```

Hoặc thông qua MySQL CLI / Workbench trên máy:
```bash
mysql -u root -p < database.sql
```
*Schema sẽ tự động tạo cơ sở dữ liệu `ttcsn` và nạp sẵn dữ liệu mẫu cho hệ thống homestay StayEasy.*

### 2. Cấu hình môi trường

Tạo hoặc chỉnh sửa file `.env` tại thư mục gốc:

```env
PORT=3000
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=ttcsn
JWT_SECRET=stayeasy_secret_key_2026_super_secure
CORS_ORIGIN=http://localhost:3000,http://127.0.0.1:3000
```

### 3. Chạy Backend & Giao diện Web

```bash
npm install
npm start
```

Mở trình duyệt truy cập: [http://localhost:3000](http://localhost:3000)

Frontend được phục vụ trực tiếp qua Express:

| Vai trò / Chức năng | Đường dẫn (URL) |
|---|---|
| Trang chủ Homestay (Chưa đăng nhập) | `http://localhost:3000/customer/trangchupre/trangchu1.html` (hoặc `/`) |
| Cổng thành viên StayEasy (Đã đăng nhập) | `http://localhost:3000/customer/trangchu/trangchu1.html` |
| Đặt homestay trực tuyến | `http://localhost:3000/customer/datphong/order1.html` |
| Quản lý homestay đã đặt của tôi | `http://localhost:3000/customer/datphong/donDatUser.html` |
| Hồ sơ thành viên & Lịch sử lưu trú | `http://localhost:3000/customer/hosoluutru/hosoluutru.html` |
| Bảng điều khiển Quản lý Homestay (Admin) | `http://localhost:3000/admin-panel/admin.html` |

### 4. Trợ lý ảo StayEasy Homestay Assistant (Tùy chọn)

```bash
pip install -r requirements.txt
uvicorn server:app --reload --port 8000
```

---

## Tài khoản mẫu trải nghiệm (Sau khi import `database.sql`)

| Vai trò | Số điện thoại | Mật khẩu mặc định | Mô tả |
|---|---|---|---|
| **Quản trị viên / Chủ Homestay** | `0900000000` | `Admin@123` | Quản lý toàn bộ hệ thống homestay StayEasy |
| **Thành viên 1** | `0912345678` | `User@1234` | Khách hàng: Nguyễn Văn An |
| **Thành viên 2** | `0987654321` | `User@1234` | Khách hàng: Trần Thị Bích |

*Mật khẩu văn bản thuần sẽ được tự động nâng cấp sang mã hóa PBKDF2 chuẩn bảo mật cao ngay lần đăng nhập đầu tiên.*

---

## Tính năng bảo mật

- **Xác thực JWT (HMAC-SHA256)**: Phân quyền nghiêm ngặt giữa Quản trị viên và Khách hàng.
- **Kiểm soát truy cập chống IDOR**: Khách hàng chỉ xem và quản lý đơn đặt homestay / hồ sơ của chính mình.
- **Giới hạn tốc độ đăng nhập (Rate Limit)**: Ngăn chặn tấn công Brute-force (tối đa 5 lần thử/phút/IP).
- **Mã hóa mật khẩu chuẩn PBKDF2**: Kèm Salt ngẫu nhiên và số vòng lặp tối ưu.
- **Chống XSS & SQL Injection**: Thoát ký tự nguy hiểm phía máy chủ và sử dụng Parameterized Queries.
- **CORS Whitelist**: Chỉ cho phép các domain được định cấu hình.
- **Ràng buộc dữ liệu chặt chẽ**: Kiểm tra ngày nhận phòng, giờ check-in, số điện thoại và định dạng mật khẩu mạnh.

---

## Cấu trúc thư mục

```
StayEasy-Homestay/
├── database.sql           # Schema cơ sở dữ liệu homestay & dữ liệu mẫu StayEasy
├── server.js              # RESTful API Express & Web Static Server (:3000)
├── package.json           # Danh sách thư viện Node.js
├── .env                   # Biến môi trường kết nối DB và JWT Secret
├── Khách hàng/            # Giao diện Cổng Khách hàng & Thành viên StayEasy Homestay
│   ├── trangchupre/       # Trang chủ giới thiệu homestay & Đăng ký / Đăng nhập
│   ├── trangchu/          # Dashboard thành viên đã đăng nhập & đổi mật khẩu
│   ├── datphong/          # Quy trình đặt phòng homestay và theo dõi đơn đặt
│   ├── hosoluutru/        # Hồ sơ thông tin thành viên & lịch sử hóa đơn lưu trú
│   └── Picture/           # Hình ảnh, banner homestay cao cấp & logo StayEasy
├── Quản trị viên/         # Bảng điều khiển Quản lý Homestay (Admin Panel)
│   ├── admin.html         # Giao diện chính Admin StayEasy Homestay
│   ├── admin-dashboard.js # Biểu đồ lượt đặt, thống kê căn và hoạt động
│   ├── admin-loaiphong.js # Quản lý Loại hình Homestay (Categories)
│   ├── admin-canphong.js  # Quản lý Danh sách căn homestay & tiện ích (Rooms)
│   ├── admin-datphong.js  # Quản lý Đơn đặt homestay (Bookings)
│   ├── admin-hosoluutru.js# Quản lý Hồ sơ khách hàng lưu trú (Guests)
│   ├── admin-lichsuluutru.js # Quản lý Lịch sử lưu trú & Hóa đơn (Stay Invoices)
│   └── admin-tkhoan.js    # Quản lý tài khoản khách hàng
├── server.py              # Dịch vụ Chatbot FastAPI Homestay (:8000)
├── chatbot.py             # Logic xử lý ngôn ngữ & trả lời Homestay Concierge Assistant
└── camnang/
    └── Homestay.md        # Cẩm nang thông tin dịch vụ, căn phòng & chính sách StayEasy Homestay
```
