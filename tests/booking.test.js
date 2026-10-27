const { test, describe, before } = require("node:test");
const assert = require("node:assert/strict");
const request = require("supertest");
const { app } = require("../server.js");

describe("Homestay Booking & Reservation Lifecycle (IEEE 829 Test Suite)", () => {
  let customerToken = "";
  let customerId = null;
  let otherCustomerToken = "";
  let otherCustomerId = null;
  let bookedBookingId = null;

  // Ngày đặt tương lai để đảm bảo hợp lệ
  const futureDate = "2027-01-15";
  const bookingHour = "14:00";

  before(async () => {
    // Đăng nhập tài khoản khách hàng mẫu 1 (idKH = 1)
    const res1 = await request(app).post("/login").send({
      sdt: "0912345678",
      matkhau: "User@1234",
    });
    assert.equal(res1.status, 200, "Đăng nhập khách hàng 1 thất bại");
    customerToken = res1.body.token;
    customerId = res1.body.user.idKH;

    // Đăng nhập tài khoản khách hàng mẫu 2 (idKH = 2) để test IDOR
    const res2 = await request(app).post("/login").send({
      sdt: "0987654321",
      matkhau: "User@1234",
    });
    assert.equal(res2.status, 200, "Đăng nhập khách hàng 2 thất bại");
    otherToken = res2.body.token;
    otherCustomerId = res2.body.user.idKH;
  });

  test("TC-BOOK-01: [Public] Lấy danh mục loại hình homestay -> HTTP 200", async () => {
    const res = await request(app).get("/api/loai-phong");
    assert.equal(res.status, 200);
    assert.ok(Array.isArray(res.body));
    assert.ok(res.body.length > 0);
    assert.ok(res.body[0].idKhoa && res.body[0].tenKhoa);
  });

  test("TC-BOOK-02: [Public] Lấy danh sách căn/phòng theo loại hình -> HTTP 200", async () => {
    const res = await request(app).get("/api/can-phong/1");
    assert.equal(res.status, 200);
    assert.ok(Array.isArray(res.body));
    assert.ok(res.body.length > 0);
  });

  test("TC-BOOK-03: [Security] Đặt phòng không cung cấp token -> HTTP 401 Unauthorized", async () => {
    const res = await request(app)
      .post("/api/dat-phong")
      .send({
        hoTen: "Khách Không Token",
        idBacSi: 1,
        idKhoa: 1,
        ngayKham: futureDate,
        gioKham: bookingHour,
      });
    assert.equal(res.status, 401);
  });

  test("TC-BOOK-04: [Negative] Đặt phòng cho ngày trong quá khứ -> HTTP 400", async () => {
    const res = await request(app)
      .post("/api/dat-phong")
      .set("Authorization", "Bearer " + customerToken)
      .send({
        hoTen: "Khách Quá Khứ",
        idBacSi: 1,
        idKhoa: 1,
        ngayKham: "2020-01-01",
        gioKham: bookingHour,
      });
    assert.equal(res.status, 400);
    assert.ok(res.body.message.includes("quá khứ"));
  });

  test("TC-BOOK-05: [Positive] Đặt phòng hợp lệ -> HTTP 200 & Tạo đơn thành công", async () => {
    const res = await request(app)
      .post("/api/dat-phong")
      .set("Authorization", "Bearer " + customerToken)
      .send({
        hoTen: "Nguyễn Văn An",
        lyDo: "Nghỉ dưỡng gia đình cuối tuần",
        idBacSi: 1,
        idKhoa: 1,
        ngayKham: futureDate,
        gioKham: bookingHour,
      });
    assert.equal(res.status, 200);
    assert.equal(res.body.success, true);
    assert.ok(res.body.idLichKham);
    bookedBookingId = res.body.idLichKham;
  });

  test("TC-BOOK-06: [Concurrency/Overbooking] Đặt trùng cùng căn phòng và khung giờ đã có người đặt -> HTTP 400", async () => {
    const res = await request(app)
      .post("/api/dat-phong")
      .set("Authorization", "Bearer " + otherToken)
      .send({
        hoTen: "Trần Thị Bích",
        lyDo: "Cố tình đặt trùng",
        idBacSi: 1,
        idKhoa: 1,
        ngayKham: futureDate,
        gioKham: bookingHour,
      });
    assert.equal(res.status, 400);
    assert.ok(res.body.message.includes("đã có khách đặt"));
  });

  test("TC-BOOK-07: [Security IDOR] Khách hàng A không được xem đơn đặt của Khách hàng B -> HTTP 403", async () => {
    const res = await request(app)
      .get("/api/don-dat-user/" + otherCustomerId)
      .set("Authorization", "Bearer " + customerToken);
    assert.equal(res.status, 403);
    assert.ok(res.body.message.includes("không có quyền xem đơn đặt của người khác"));
  });

  test("TC-BOOK-08: [Positive] Khách hàng xem đúng danh sách đơn đặt của chính mình -> HTTP 200", async () => {
    const res = await request(app)
      .get("/api/don-dat-user/" + customerId)
      .set("Authorization", "Bearer " + customerToken);
    assert.equal(res.status, 200);
    assert.ok(Array.isArray(res.body));
    const createdBooking = res.body.find(b => b.idLichKham === bookedBookingId);
    assert.ok(createdBooking, "Không tìm thấy đơn đặt vừa tạo trong danh sách");
  });

  test("TC-BOOK-09: [Security IDOR] Khách hàng A không thể hủy đơn đặt của Khách hàng B -> HTTP 403", async () => {
    const res = await request(app)
      .post("/api/huy-dat-phong")
      .set("Authorization", "Bearer " + otherToken)
      .send({ idDatPhong: bookedBookingId });
    assert.equal(res.status, 403);
    assert.ok(res.body.message.includes("không có quyền hủy đơn đặt phòng của người khác"));
  });

  test("TC-BOOK-10: [Positive] Khách hàng hủy đơn đặt của chính mình -> HTTP 200", async () => {
    const res = await request(app)
      .post("/api/huy-dat-phong")
      .set("Authorization", "Bearer " + customerToken)
      .send({ idDatPhong: bookedBookingId });
    assert.equal(res.status, 200);
    assert.equal(res.body.success, true);
  });

  test("TC-BOOK-11: [Negative] Hủy lại đơn đã được hủy trước đó -> HTTP 400", async () => {
    const res = await request(app)
      .post("/api/huy-dat-phong")
      .set("Authorization", "Bearer " + customerToken)
      .send({ idDatPhong: bookedBookingId });
    assert.equal(res.status, 400);
    assert.ok(res.body.message.includes("đã được hủy trước đó"));
  });
});
