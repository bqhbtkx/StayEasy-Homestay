-- =========================================================================
-- Schema hệ thống quản lý và đặt phòng homestay StayEasy (Database: ttcsn)
-- Chạy: docker exec -i mysql-ktpm mysql -uroot -proot ttcsn < database.sql
-- =========================================================================

CREATE DATABASE IF NOT EXISTS ttcsn
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE ttcsn;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS LICHSUKHAMBENH;
DROP TABLE IF EXISTS LICHKHAM;
DROP TABLE IF EXISTS HOSOYTE;
DROP TABLE IF EXISTS BACSI;
DROP TABLE IF EXISTS KHOA;
DROP TABLE IF EXISTS hoatdong;
DROP TABLE IF EXISTS KHACHHANG;
DROP TABLE IF EXISTS QUANTRIVIEN;

SET FOREIGN_KEY_CHECKS = 1;

-- ================== 1. QUẢN TRỊ VIÊN / QUẢN LÝ HOMESTAY ==================
CREATE TABLE QUANTRIVIEN (
  idQTV INT AUTO_INCREMENT PRIMARY KEY,
  sdtQTV VARCHAR(11) NOT NULL UNIQUE,
  matKhauQTV VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================== 2. KHÁCH HÀNG / THÀNH VIÊN HOMESTAY ==================
CREATE TABLE KHACHHANG (
  idKH INT AUTO_INCREMENT PRIMARY KEY,
  hoTen VARCHAR(100) NOT NULL,
  sdt VARCHAR(11) NOT NULL UNIQUE,
  matKhau VARCHAR(255) NOT NULL,
  gioiTinh VARCHAR(10) DEFAULT NULL,
  ngayThangNamSinh DATE DEFAULT NULL,
  cccd VARCHAR(20) DEFAULT NULL,
  diaChi VARCHAR(255) DEFAULT NULL,
  INDEX idx_kh_sdt (sdt)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================== 3. LOẠI HÌNH HOMESTAY (KHOA) ==================
CREATE TABLE KHOA (
  idKhoa INT AUTO_INCREMENT PRIMARY KEY,
  tenKhoa VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================== 4. DANH SÁCH CĂN / PHÒNG HOMESTAY (BACSI) ==================
CREATE TABLE BACSI (
  idBacSi INT AUTO_INCREMENT PRIMARY KEY,
  hoTenBacSi VARCHAR(100) NOT NULL,     -- Tên căn / phòng (VD: Bungalow 01 - Hoa Đậu Biếc)
  hocVi VARCHAR(100) DEFAULT NULL,       -- Tiện nghi & Mức giá (VD: 1 Giường Queen, Bếp BBQ • 650.000đ/đêm)
  idKhoa INT NOT NULL,                  -- Mã loại hình homestay
  CONSTRAINT fk_bacsi_khoa FOREIGN KEY (idKhoa) REFERENCES KHOA(idKhoa)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  INDEX idx_bacsi_khoa (idKhoa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================== 5. HỒ SƠ KHÁCH LƯU TRÚ / THÀNH VIÊN (HOSOYTE) ==================
CREATE TABLE HOSOYTE (
  idHoSoYTe INT AUTO_INCREMENT PRIMARY KEY,
  idKH INT NOT NULL UNIQUE,
  CONSTRAINT fk_hoso_kh FOREIGN KEY (idKH) REFERENCES KHACHHANG(idKH)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================== 6. ĐƠN ĐẶT PHÒNG HOMESTAY (LICHKHAM) ==================
CREATE TABLE LICHKHAM (
  idLichKham INT AUTO_INCREMENT PRIMARY KEY,
  hoTen VARCHAR(100) NOT NULL,              -- Người đại diện nhận phòng
  lyDo TEXT,                                -- Ghi chú đặt phòng / Yêu cầu đặc biệt (tiệc BBQ, bếp tự nấu...)
  ngayKham DATE NOT NULL,                   -- Ngày nhận phòng (Check-in)
  gioKham TIME NOT NULL,                    -- Giờ nhận phòng dự kiến (VD: 14:00:00)
  idKH INT NOT NULL,                        -- ID khách hàng đặt
  idBacSi INT NOT NULL,                     -- ID căn/phòng đã chọn
  idKhoa INT NOT NULL,                      -- ID loại hình homestay
  trangThai VARCHAR(50) NOT NULL DEFAULT 'chờ xác nhận',
  CONSTRAINT fk_lich_kh FOREIGN KEY (idKH) REFERENCES KHACHHANG(idKH)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_lich_bs FOREIGN KEY (idBacSi) REFERENCES BACSI(idBacSi)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_lich_khoa FOREIGN KEY (idKhoa) REFERENCES KHOA(idKhoa)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  INDEX idx_lich_bs_ngay_gio (idBacSi, ngayKham, gioKham),
  INDEX idx_lich_kh (idKH),
  INDEX idx_lich_status (trangThai)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================== 7. LỊCH SỬ LƯU TRÚ & HÓA ĐƠN (LICHSUKHAMBENH) ==================
CREATE TABLE LICHSUKHAMBENH (
  idLS INT AUTO_INCREMENT PRIMARY KEY,
  ngayKham DATE NOT NULL,                   -- Ngày trả phòng / Check-out
  ketLuan VARCHAR(255) NOT NULL,            -- Tình trạng lưu trú & Đánh giá (VD: Hoàn tất 3N2Đ - Khách đánh giá 5 sao)
  chiTiet TEXT,                             -- Chi tiết hóa đơn & dịch vụ sử dụng
  idBacSi INT NOT NULL,                     -- Căn/phòng đã lưu trú
  idKhoa INT NOT NULL,                      -- Loại hình homestay
  idHoSoYTe INT NOT NULL,                   -- Hồ sơ thành viên
  CONSTRAINT fk_ls_bs FOREIGN KEY (idBacSi) REFERENCES BACSI(idBacSi)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_ls_khoa FOREIGN KEY (idKhoa) REFERENCES KHOA(idKhoa)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_ls_hoso FOREIGN KEY (idHoSoYTe) REFERENCES HOSOYTE(idHoSoYTe)
    ON UPDATE CASCADE ON DELETE CASCADE,
  INDEX idx_ls_hoso (idHoSoYTe)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================== 8. NHẬT KÝ HOẠT ĐỘNG HOMESTAY (hoatdong) ==================
CREATE TABLE hoatdong (
  id INT AUTO_INCREMENT PRIMARY KEY,
  loaiHoatDong VARCHAR(100) NOT NULL,
  moTa VARCHAR(500) NOT NULL,
  idNguoiThucHien INT DEFAULT NULL,
  thoiGian DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_hd_time (thoiGian)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================== DỮ LIỆU MẪU STAYEASY HOMESTAY ==================
-- Quản lý / Chủ homestay: 0900000000 / Admin@123
-- Khách đặt phòng 1: 0912345678 / User@1234
-- Khách đặt phòng 2: 0987654321 / User@1234

INSERT INTO QUANTRIVIEN (sdtQTV, matKhauQTV) VALUES
('0900000000', 'Admin@123');

INSERT INTO KHACHHANG (hoTen, sdt, matKhau, gioiTinh, ngayThangNamSinh, cccd, diaChi) VALUES
('Nguyễn Văn An', '0912345678', 'User@1234', 'Nam', '1995-04-15', '001095012345', 'Hà Nội'),
('Trần Thị Bích', '0987654321', 'User@1234', 'Nữ', '1998-09-22', '001298098765', 'Đà Nẵng'),
('Lê Hoàng Nam', '0933221100', 'User@1234', 'Nam', '1992-11-05', '079092003456', 'TP. Hồ Chí Minh');

INSERT INTO HOSOYTE (idKH) VALUES (1), (2), (3);

-- Các loại hình Homestay tại StayEasy
INSERT INTO KHOA (tenKhoa) VALUES
('Bungalow Sân Vườn Chill'),
('Phòng Gỗ Thông Vintage'),
('Phòng Áp Mái Panorama View'),
('Villa Nguyên Căn Có Hồ Bơi'),
('Glamping Lều Trại Cao Cấp');

-- Danh sách căn/phòng chi tiết
INSERT INTO BACSI (hoTenBacSi, hocVi, idKhoa) VALUES
('Bungalow 01 - Hoa Đậu Biếc', '1 Giường Queen, Bếp nướng BBQ ngoài trời, View vườn hoa • 650.000đ/đêm', 1),
('Bungalow 02 - Hướng Dương', '2 Giường đơn, Sân hiên uống trà, Bếp tự nấu • 750.000đ/đêm', 1),
('Nhà Gỗ 101 - Rừng Thông', '1 Giường King, Lò sưởi ấm cúng, Ban công ngắm đồi • 900.000đ/đêm', 2),
('Nhà Gỗ 102 - Suối Mơ', '1 Giường King, Bồn tắm gỗ ngoài trời, View suối reo • 1.100.000đ/đêm', 2),
('Áp Mái 201 - Hoàng Hôn (Sunset Loft)', 'Giường nệm êm ái, Cửa sổ kính ngắm sao, Máy chiếu phim • 850.000đ/đêm', 3),
('Áp Mái 202 - Bình Minh (Sunrise Loft)', 'Ban công kính toàn cảnh, Góc trà chill, Bồn tắm nằm • 950.000đ/đêm', 3),
('Villa 301 - Panorama Hill (Nguyên Căn)', '3 Phòng ngủ, Hồ bơi vô cực, Khu BBQ, Bếp đầy đủ gia vị • 3.500.000đ/đêm', 4),
('Glamping 401 - Lều Trại Sao Băng', 'Lều cao cấp chống nước, Đệm ấm, Khu lửa trại, Tiệc nướng BBQ • 550.000đ/đêm', 5);

-- Lịch sử lưu trú mẫu
INSERT INTO LICHSUKHAMBENH (ngayKham, ketLuan, chiTiet, idBacSi, idKhoa, idHoSoYTe) VALUES
('2026-09-20', 'Hoàn tất kỳ nghỉ chill 3N2Đ - Khách đánh giá 5 sao ⭐⭐⭐⭐⭐', 'Bungalow 01 - Hoa Đậu Biếc. Dịch vụ: Set tiệc nướng BBQ sân vườn, Thuê xe máy ngắm đồi mây, Check-out đúng giờ. Tổng tiền: 1.650.000đ.', 1, 1, 1),
('2026-10-02', 'Kỳ nghỉ cuối tuần chữa lành - Rất hài lòng ⭐⭐⭐⭐⭐', 'Nhà Gỗ 101 - Rừng Thông. Dịch vụ: Bữa sáng nông trại organic, Đốt lửa trại & khoai nướng, Cà phê ngắm sương. Tổng tiền: 1.250.000đ.', 3, 2, 2);

-- Đơn đặt phòng mẫu sắp tới
INSERT INTO LICHKHAM (hoTen, lyDo, ngayKham, gioKham, idKH, idBacSi, idKhoa, trangThai) VALUES
('Nguyễn Văn An', 'Đi trốn phố thị cuối tuần 2 người, cần chuẩn bị sẵn bếp nướng than BBQ ngoài trời', DATE_ADD(CURDATE(), INTERVAL 1 DAY), '14:00:00', 1, 1, 1, 'chờ xác nhận'),
('Trần Thị Bích', 'Đi cùng gia đình nhóm 6 người, cần nôi em bé và hỗ trợ chuẩn bị tiệc BBQ hồ bơi', DATE_ADD(CURDATE(), INTERVAL 2 DAY), '15:00:00', 2, 7, 4, 'đã xác nhận');

-- Hoạt động mẫu
INSERT INTO hoatdong (loaiHoatDong, moTa, idNguoiThucHien, thoiGian) VALUES
('Hệ thống', 'Khởi tạo hệ thống quản lý homestay StayEasy thành công', 1, NOW()),
('Đặt phòng', 'Khách hàng Nguyễn Văn An vừa đặt Bungalow 01 - Hoa Đậu Biếc', 1, NOW());
