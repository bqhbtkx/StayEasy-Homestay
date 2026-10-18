-- =========================================================================
-- STAYEASY HOMESTAY - CƠ SỞ DỮ LIỆU HỆ THỐNG ĐẶT PHÒNG & NGHỈ DƯỠNG
-- Database Name: ttcsn
-- Tương thích: MySQL 5.7+ / MySQL 8.0+ / MariaDB
-- Lệnh import: docker exec -i mysql-ktpm mysql -uroot -proot ttcsn < database.sql
-- =========================================================================

CREATE DATABASE IF NOT EXISTS ttcsn
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE ttcsn;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- -------------------------------------------------------------------------
-- 0. Xóa các View và Bảng cũ nếu đã tồn tại
-- -------------------------------------------------------------------------
DROP VIEW IF EXISTS LICHSUKHAMBENH;
DROP VIEW IF EXISTS LICHKHAM;
DROP VIEW IF EXISTS HOSOYTE;
DROP VIEW IF EXISTS BACSI;
DROP VIEW IF EXISTS KHOA;

DROP TABLE IF EXISTS LICHSULUUTRU;
DROP TABLE IF EXISTS DATPHONG;
DROP TABLE IF EXISTS HOSOLUUTRU;
DROP TABLE IF EXISTS CANPHONG;
DROP TABLE IF EXISTS LOAIPHONG;
DROP TABLE IF EXISTS hoatdong;
DROP TABLE IF EXISTS KHACHHANG;
DROP TABLE IF EXISTS QUANTRIVIEN;

-- Đề phòng các bảng theo tên cũ
DROP TABLE IF EXISTS LICHSUKHAMBENH_OLD;
DROP TABLE IF EXISTS LICHKHAM_OLD;
DROP TABLE IF EXISTS HOSOYTE_OLD;
DROP TABLE IF EXISTS BACSI_OLD;
DROP TABLE IF EXISTS KHOA_OLD;

SET FOREIGN_KEY_CHECKS = 1;

-- =========================================================================
-- 1. BẢNG QUẢN TRỊ VIÊN / CHỦ HOMESTAY (QUANTRIVIEN)
-- =========================================================================
CREATE TABLE QUANTRIVIEN (
  idQTV INT AUTO_INCREMENT PRIMARY KEY,
  sdtQTV VARCHAR(11) NOT NULL UNIQUE,
  matKhauQTV VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================================================
-- 2. BẢNG KHÁCH HÀNG / THÀNH VIÊN (KHACHHANG)
-- =========================================================================
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

-- =========================================================================
-- 3. BẢNG DANH MỤC LOẠI HÌNH PHÒNG / HOMESTAY (LOAIPHONG)
-- =========================================================================
CREATE TABLE LOAIPHONG (
  idLoaiPhong INT AUTO_INCREMENT PRIMARY KEY,
  tenLoaiPhong VARCHAR(100) NOT NULL UNIQUE,
  moTa TEXT DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================================================
-- 4. BẢNG DANH SÁCH CĂN / PHÒNG NGHỈ DƯỠNG (CANPHONG)
-- =========================================================================
CREATE TABLE CANPHONG (
  idCanPhong INT AUTO_INCREMENT PRIMARY KEY,
  tenCanPhong VARCHAR(100) NOT NULL,
  tienNghiGia VARCHAR(255) DEFAULT NULL,
  idLoaiPhong INT NOT NULL,
  CONSTRAINT fk_canphong_loaiphong FOREIGN KEY (idLoaiPhong) REFERENCES LOAIPHONG(idLoaiPhong)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  INDEX idx_canphong_loai (idLoaiPhong)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================================================
-- 5. BẢNG HỒ SƠ LƯU TRÚ / THÀNH VIÊN CỦA KHÁCH (HOSOLUUTRU)
-- =========================================================================
CREATE TABLE HOSOLUUTRU (
  idHoSoLuuTru INT AUTO_INCREMENT PRIMARY KEY,
  idKH INT NOT NULL,
  CONSTRAINT fk_hosoluutru_khachhang FOREIGN KEY (idKH) REFERENCES KHACHHANG(idKH)
    ON UPDATE CASCADE ON DELETE CASCADE,
  INDEX idx_hosoluutru_kh (idKH)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================================================
-- 6. BẢNG ĐƠN ĐẶT PHÒNG HOMESTAY (DATPHONG)
-- =========================================================================
CREATE TABLE DATPHONG (
  idDatPhong INT AUTO_INCREMENT PRIMARY KEY,
  hoTen VARCHAR(100) NOT NULL,
  ghiChu VARCHAR(255) DEFAULT NULL,
  ngayNhanPhong DATE NOT NULL,
  gioNhanPhong TIME NOT NULL,
  idKH INT NOT NULL,
  idCanPhong INT NOT NULL,
  idLoaiPhong INT NOT NULL,
  trangThai VARCHAR(50) DEFAULT 'chờ xác nhận',
  CONSTRAINT fk_datphong_khachhang FOREIGN KEY (idKH) REFERENCES KHACHHANG(idKH)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_datphong_canphong FOREIGN KEY (idCanPhong) REFERENCES CANPHONG(idCanPhong)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_datphong_loaiphong FOREIGN KEY (idLoaiPhong) REFERENCES LOAIPHONG(idLoaiPhong)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  INDEX idx_dp_kh (idKH),
  INDEX idx_dp_can (idCanPhong),
  INDEX idx_dp_loai (idLoaiPhong),
  INDEX idx_dp_ngay (ngayNhanPhong)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================================================
-- 7. BẢNG LỊCH SỬ LƯU TRÚ & ĐÁNH GIÁ (LICHSULUUTRU)
-- =========================================================================
CREATE TABLE LICHSULUUTRU (
  idLichSu INT AUTO_INCREMENT PRIMARY KEY,
  ngayTraPhong DATE NOT NULL,
  danhGia VARCHAR(255) DEFAULT NULL,
  chiTietHoaDon TEXT DEFAULT NULL,
  idCanPhong INT NOT NULL,
  idLoaiPhong INT NOT NULL,
  idHoSoLuuTru INT NOT NULL,
  CONSTRAINT fk_ls_canphong FOREIGN KEY (idCanPhong) REFERENCES CANPHONG(idCanPhong)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_ls_loaiphong FOREIGN KEY (idLoaiPhong) REFERENCES LOAIPHONG(idLoaiPhong)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_ls_hosoluutru FOREIGN KEY (idHoSoLuuTru) REFERENCES HOSOLUUTRU(idHoSoLuuTru)
    ON UPDATE CASCADE ON DELETE CASCADE,
  INDEX idx_ls_can (idCanPhong),
  INDEX idx_ls_loai (idLoaiPhong),
  INDEX idx_ls_hoso (idHoSoLuuTru)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================================================
-- 8. BẢNG NHẬT KÝ HOẠT ĐỘNG HỆ THỐNG (hoatdong)
-- =========================================================================
CREATE TABLE hoatdong (
  id INT AUTO_INCREMENT PRIMARY KEY,
  loaiHoatDong VARCHAR(100) NOT NULL,
  moTa VARCHAR(500) NOT NULL,
  idNguoiThucHien INT DEFAULT NULL,
  thoiGian DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_hd_time (thoiGian)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =========================================================================
-- 9. TẠO CÁC VIEW TƯƠNG THÍCH NGƯỢC (Tương thích với các truy vấn legacy)
-- =========================================================================
CREATE OR REPLACE VIEW KHOA AS
  SELECT 
    idLoaiPhong AS idKhoa, 
    tenLoaiPhong AS tenKhoa 
  FROM LOAIPHONG;

CREATE OR REPLACE VIEW BACSI AS
  SELECT 
    idCanPhong AS idBacSi, 
    tenCanPhong AS hoTenBacSi, 
    tienNghiGia AS hocVi, 
    idLoaiPhong AS idKhoa 
  FROM CANPHONG;

CREATE OR REPLACE VIEW HOSOYTE AS
  SELECT 
    idHoSoLuuTru AS idHoSoYTe, 
    idKH 
  FROM HOSOLUUTRU;

CREATE OR REPLACE VIEW LICHKHAM AS
  SELECT 
    idDatPhong AS idLichKham, 
    hoTen, 
    ghiChu AS lyDo, 
    ngayNhanPhong AS ngayKham, 
    gioNhanPhong AS gioKham, 
    idKH, 
    idCanPhong AS idBacSi, 
    idLoaiPhong AS idKhoa, 
    trangThai 
  FROM DATPHONG;

CREATE OR REPLACE VIEW LICHSUKHAMBENH AS
  SELECT 
    idLichSu AS idLichSuKham, 
    ngayTraPhong AS ngayKham, 
    danhGia AS ketLuan, 
    chiTietHoaDon AS chiTiet, 
    idCanPhong AS idBacSi, 
    idLoaiPhong AS idKhoa, 
    idHoSoLuuTru AS idHoSoYTe 
  FROM LICHSULUUTRU;

-- =========================================================================
-- 10. DỮ LIỆU KHỞI TẠO MẪU (SEED DATA)
-- =========================================================================

-- Tài khoản quản trị viên / chủ homestay (0900000000 / Admin@123)
INSERT INTO QUANTRIVIEN (sdtQTV, matKhauQTV) VALUES
('0900000000', 'Admin@123');

-- Khách hàng mẫu (Mật khẩu: User@1234)
INSERT INTO KHACHHANG (hoTen, sdt, matKhau, gioiTinh, ngayThangNamSinh, cccd, diaChi) VALUES
('Nguyễn Văn An', '0912345678', 'User@1234', 'Nam', '1995-04-15', '001095012345', 'Hà Nội'),
('Trần Thị Bích', '0987654321', 'User@1234', 'Nữ', '1998-09-22', '001298098765', 'Đà Nẵng'),
('Lê Hoàng Nam', '0933221100', 'User@1234', 'Nam', '1992-11-05', '079092003456', 'TP. Hồ Chí Minh');

-- Hồ sơ lưu trú của khách
INSERT INTO HOSOLUUTRU (idKH) VALUES (1), (2), (3);

-- Danh mục loại hình Homestay
INSERT INTO LOAIPHONG (tenLoaiPhong, moTa) VALUES
('Bungalow Sân Vườn Chill', 'Căn nhà gỗ biệt lập có sân vườn thoáng mát, hoa cỏ và bếp nướng than BBQ ngoài trời'),
('Phòng Gỗ Thông Vintage', 'Không gian gỗ thông Đà Lạt ấm áp, lò sưởi củi và ban công ngắm sương mù đồi thông'),
('Phòng Áp Mái Panorama View', 'Căn áp mái lãng mạn với cửa sổ kính đón trọn hoàng hôn và ngắm bầu trời đêm'),
('Villa Nguyên Căn Có Hồ Bơi', 'Biệt thự nghỉ dưỡng cao cấp có hồ bơi vô cực, bếp nấu tiện nghi cho gia đình và nhóm bạn'),
('Glamping Lều Trại Cao Cấp', 'Trải nghiệm cắm trại sang trọng giữa thiên nhiên hoang sơ, tiệc BBQ và lửa trại');

-- Danh sách căn/phòng chi tiết kèm tiện nghi và giá
INSERT INTO CANPHONG (tenCanPhong, tienNghiGia, idLoaiPhong) VALUES
('Bungalow 01 - Hoa Đậu Biếc', '1 Giường Queen, Bếp nướng BBQ ngoài trời, View vườn hoa • 650.000đ/đêm', 1),
('Bungalow 02 - Hướng Dương', '2 Giường đơn, Sân hiên uống trà, Bếp tự nấu • 750.000đ/đêm', 1),
('Nhà Gỗ 101 - Rừng Thông', '1 Giường King, Lò sưởi ấm cúng, Ban công ngắm đồi • 900.000đ/đêm', 2),
('Nhà Gỗ 102 - Suối Mơ', '1 Giường King, Bồn tắm gỗ ngoài trời, View suối reo • 1.100.000đ/đêm', 2),
('Áp Mái 201 - Hoàng Hôn (Sunset Loft)', 'Giường nệm êm ái, Cửa sổ kính ngắm sao, Máy chiếu phim • 850.000đ/đêm', 3),
('Áp Mái 202 - Bình Minh (Sunrise Loft)', 'Ban công kính toàn cảnh, Góc trà chill, Bồn tắm nằm • 950.000đ/đêm', 3),
('Villa 301 - Panorama Hill (Nguyên Căn)', '3 Phòng ngủ, Hồ bơi vô cực, Khu BBQ, Bếp đầy đủ gia vị • 3.500.000đ/đêm', 4),
('Glamping 401 - Lều Trại Sao Băng', 'Lều cao cấp chống nước, Đệm ấm, Khu lửa trại, Tiệc nướng BBQ • 550.000đ/đêm', 5);

-- Lịch sử lưu trú mẫu
INSERT INTO LICHSULUUTRU (ngayTraPhong, danhGia, chiTietHoaDon, idCanPhong, idLoaiPhong, idHoSoLuuTru) VALUES
('2026-09-20', 'Hoàn tất kỳ nghỉ chill 3N2Đ - Khách đánh giá 5 sao ⭐⭐⭐⭐⭐', 'Bungalow 01 - Hoa Đậu Biếc. Dịch vụ: Set tiệc nướng BBQ sân vườn, Thuê xe máy ngắm đồi mây, Check-out đúng giờ. Tổng tiền: 1.650.000đ.', 1, 1, 1),
('2026-10-02', 'Kỳ nghỉ cuối tuần chữa lành - Rất hài lòng ⭐⭐⭐⭐⭐', 'Nhà Gỗ 101 - Rừng Thông. Dịch vụ: Bữa sáng nông trại organic, Đốt lửa trại & khoai nướng, Cà phê ngắm sương. Tổng tiền: 1.250.000đ.', 3, 2, 2);

-- Đơn đặt phòng mẫu sắp tới
INSERT INTO DATPHONG (hoTen, ghiChu, ngayNhanPhong, gioNhanPhong, idKH, idCanPhong, idLoaiPhong, trangThai) VALUES
('Nguyễn Văn An', 'Đi trốn phố thị cuối tuần 2 người, cần chuẩn bị sẵn bếp nướng than BBQ ngoài trời', DATE_ADD(CURDATE(), INTERVAL 1 DAY), '14:00:00', 1, 1, 1, 'chờ xác nhận'),
('Trần Thị Bích', 'Đi cùng gia đình nhóm 6 người, cần nôi em bé và hỗ trợ chuẩn bị tiệc BBQ hồ bơi', DATE_ADD(CURDATE(), INTERVAL 2 DAY), '15:00:00', 2, 7, 4, 'đã xác nhận');

-- Hoạt động mẫu
INSERT INTO hoatdong (loaiHoatDong, moTa, idNguoiThucHien, thoiGian) VALUES
('Hệ thống', 'Khởi tạo hệ thống quản lý homestay StayEasy thành công', 1, NOW()),
('Đặt phòng', 'Khách hàng Nguyễn Văn An vừa đặt Bungalow 01 - Hoa Đậu Biếc', 1, NOW());
