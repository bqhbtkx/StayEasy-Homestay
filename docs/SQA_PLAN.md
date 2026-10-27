# KẾ HOẠCH ĐẢM BẢO CHẤT LƯỢNG PHẦN MỀM (SQA PLAN)
## DỰ ÁN: HỆ THỐNG ĐẶT PHÒNG HOMESTAY STAYEASY (STAYEASY-HOMESTAY)
**Tiêu chuẩn tuân thủ:** IEEE Std 730™-2014 (IEEE Standard for Software Quality Assurance Processes)  
**Phiên bản tài liệu:** 1.0  
**Ngày phê duyệt:** 23/10/2026  
**Chủ trì SQA:** Senior Software Quality Engineer & Architect  

---

## 1. MỤC TIÊU VÀ PHẠM VI (PURPOSE AND SCOPE)

### 1.1. Mục tiêu
Kế hoạch SQA này thiết lập quy trình, chuẩn mực kỹ thuật và tiêu chí đánh giá chất lượng cho toàn bộ vòng đời phát triển và bảo trì hệ thống **StayEasy Homestay**. Mục tiêu chính:
1. Đảm bảo phần mềm tuân thủ nghiêm ngặt 8 đặc tính chất lượng theo **ISO/IEC 25010:2011**.
2. Kiểm soát các rủi ro bảo mật (CWE/OWASP Top 10), loại bỏ nguy cơ rò rỉ dữ liệu, Overbooking và Broken Access Control (IDOR).
3. Đảm bảo toàn bộ quy trình kiểm thử và tạo tài liệu kiểm thử tuân thủ **IEEE 829:2008**.
4. Thiết lập chốt chặn chất lượng tự động hóa (Quality Gates) qua CI/CD trước khi phát hành mã nguồn.

### 1.2. Phạm vi áp dụng
- **Backend API:** Toàn bộ RESTful API viết trên Node.js/Express (`server.js`).
- **Cơ sở dữ liệu:** Schema MySQL, các bảng dữ liệu, ràng buộc quan hệ, View và Index (`database.sql`).
- **Frontend Web:** Giao diện đặt phòng khách hàng (`Khách hàng/`) và bảng điều khiển quản trị (`Quản trị viên/`).
- **Môi trường:** Local Development, CI Testing Container và Production Staging.

---

## 2. TÀI LIỆU VÀ TIÊU CHUẨN THAM CHIẾU (REFERENCE STANDARDS)

1. **ISO/IEC 25010:2011**: Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models.
2. **IEEE Std 730-2014**: IEEE Standard for Software Quality Assurance Processes.
3. **IEEE Std 829-2008**: IEEE Standard for Software and System Test Documentation.
4. **OWASP Top 10 - 2021**: The Ten Most Critical Web Application Security Risks.
5. **CWE (Common Weakness Enumeration)**: CWE-942 (Permissive CORS), CWE-79 (XSS), CWE-639 (IDOR), CWE-400 (Resource Exhaustion).

---

## 3. VAI TRÒ VÀ TRÁCH NHIỆM (ROLES AND RESPONSIBILITIES)

| Vai trò | Thành viên / Vị trí | Trách nhiệm chính |
| :--- | :--- | :--- |
| **SQA Lead / Security Engineer** | Senior Quality Engineer | Soạn thảo SQA Plan, phê duyệt Quality Gates, kiểm tra an toàn mã nguồn, rà soát lỗ hổng bảo mật. |
| **Software Architect** | Senior Architect | Thiết kế kiến trúc module, rà soát transaction boundaries, concurrency control, tối ưu hóa CSDL. |
| **Backend / Frontend Developer** | Development Team | Triển khai code tuân thủ Coding Guidelines, sửa lỗi theo Incident Report, viết unit test đi kèm. |
| **QA / Test Engineer** | Testing Team | Thiết kế kịch bản test (Test Design/Specification), chạy tự động hóa regression test theo IEEE 829. |

---

## 4. HOẠT ĐỘNG REVIEW VÀ AUDIT (REVIEWS AND AUDITS)

### 4.1. Peer Code Review Checklist
Mọi Pull Request (PR) phải được ít nhất 1 Senior Engineer duyệt với checklist:
- [ ] Không có SQL query nối chuỗi (bắt buộc dùng Parameterized Queries `?`).
- [ ] Kiểm tra phân quyền và IDOR trên mọi endpoint nhận tham số `idKH` / `idDatPhong`.
- [ ] Không có hàm đồng bộ chặn luồng xử lý CPU cao (như `pbkdf2Sync`) trong request handler.
- [ ] Các thao tác ghi CSDL nhiều bảng bắt buộc nằm trong Transaction có `commit` và `rollback` đầy đủ.
- [ ] Mọi Map / Set lưu trữ in-memory phải có cơ chế dọn dẹp TTL để chống rò rỉ bộ nhớ.
- [ ] Bổ sung test case tự động kiểm chứng cho chức năng mới hoặc bug được sửa.

### 4.2. SQA Process Audit
- Định kỳ hàng tuần audit trạng thái dependencies (`npm audit`).
- Đánh giá chỉ số test pass rate (yêu cầu đạt 100% test pass trước khi đóng sprint).

---

## 5. QUY TRÌNH QUẢN LÝ LỖI (DEFECT MANAGEMENT)

### 5.1. Phân loại mức độ nghiêm trọng (Defect Severity)
- **P0 (Critical):** Lỗ hổng bảo mật nguy hiểm (IDOR, lộ Secret, Bypass Auth), lỗi sai lệch dữ liệu tài chính/đặt phòng (Overbooking, Deadlock). Thời gian xử lý: < 4 giờ.
- **P1 (High):** Chức năng chính bị lỗi, memory leak, nghẽn hiệu năng làm tăng độ trễ > 500ms, thiếu xử lý ngoại lệ gây crash process. Thời gian xử lý: < 24 giờ.
- **P2 (Medium):** Lỗi UI/UX cục bộ, thiếu log hoạt động, cấu hình chưa tối ưu. Thời gian xử lý: Trong sprint hiện tại.
- **P3 (Low):** Vấn đề nhỏ về naming convention, cú pháp, khoảng trắng, tài liệu chưa đầy đủ.

### 5.2. Vòng đời của lỗi (Defect Lifecycle)
```
[New] ──> [Assigned] ──> [In Progress] ──> [Fixed] ──> [Verified via Test] ──> [Closed]
                                              │
                                              └──> [Failed Re-test] ──> [Re-opened]
```

---

## 6. QUẢN LÝ CẤU HÌNH VÀ THAY ĐỔI (CONFIGURATION & CHANGE CONTROL)

1. **Quản lý phiên bản (Git):**
   - Nhánh `main`: Chứa mã nguồn ổn định sẵn sàng phát hành.
   - Nhánh `ver-2`: Nhánh phát triển chính cho phiên bản StayEasy Homestay.
   - Không commit trực tiếp secret, password, key vào Git repository. Bắt buộc dùng `.env` và cung cấp `.env.example`.
2. **Kiểm soát Dependency:**
   - File `package-lock.json` được khóa phiên bản chính xác để đảm bảo tính tái lập (Reproducibility).
   - Tự động quét lỗ hổng dependency thông qua lệnh `npm audit --audit-level=critical` trong CI pipeline.

---

## 7. CHỐT CHẶN CHẤT LƯỢNG (QUALITY GATES)

Mã nguồn chỉ được chấp thuận sáp nhập (merge) và triển khai (deploy) khi thỏa mãn 100% các tiêu chí sau:

| STT | Tiêu chí Quality Gate | Ngưỡng bắt buộc | Phương pháp đo lường | Trạng thái hiện tại |
| :---: | :--- | :---: | :--- | :---: |
| **QG-1** | Automated Test Suite Pass Rate | **100%** | `npm test` (36/36 test cases pass) | **ĐẠT (36/36 PASS)** |
| **QG-2** | Critical & High Vulnerabilities | **0 lỗi** | `npm audit` | **ĐẠT (0 Critical, 0 High ở runtime)** |
| **QG-3** | Endpoint Health Check | **200 OK** | `GET /api/health` -> `status: healthy` | **ĐẠT** |
| **QG-4** | Concurrency Safety (Overbooking) | **Không bị trùng** | `TC-BOOK-06` chạy đồng thời | **ĐẠT (Locking Verified)** |
| **QG-5** | Memory Leak Free (Rate Limiter) | **TTL Sweep Active** | Quản lý vòng đời Map với interval unref | **ĐẠT** |
| **QG-6** | IDOR Security Protection | **100% Enforced** | Khách chỉ xem/hủy đơn của chính mình | **ĐẠT (TC-BOOK-07, TC-BOOK-09)** |

---

## 8. QUY TRÌNH PHÁT HÀNH (RELEASE PROCESS)

1. Chạy toàn bộ bộ test hồi quy tự động cục bộ: `npm test`.
2. Khởi tạo container MySQL test và xác nhận schema `database.sql` import thành công không lỗi cú pháp.
3. Kiểm tra biến môi trường `.env` có khóa bí mật mạnh và CORS origin cụ thể.
4. Push mã nguồn lên remote repository để kích hoạt GitHub Actions CI Pipeline.
5. Khi pipeline CI báo trạng thái **GREEN (All Checks Passed)**, tiến hành gắn thẻ phiên bản Git tag (ví dụ: `v2.0.0`).
