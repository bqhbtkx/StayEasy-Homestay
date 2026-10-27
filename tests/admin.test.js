const { test, describe, before } = require("node:test");
const assert = require("node:assert/strict");
const request = require("supertest");
const { app } = require("../server.js");

describe("Admin Operations & Role-based Access Control (IEEE 829 Test Suite)", () => {
  let adminToken = "";
  let customerToken = "";
  let createdCategoryId = null;

  before(async () => {
    // Đăng nhập Admin
    const adminRes = await request(app).post("/login").send({
      sdt: "0900000000",
      matkhau: "Admin@123",
    });
    assert.equal(adminRes.status, 200, "Đăng nhập Admin thất bại");
    adminToken = adminRes.body.token;

    // Đăng nhập Customer
    const userRes = await request(app).post("/login").send({
      sdt: "0912345678",
      matkhau: "User@1234",
    });
    assert.equal(userRes.status, 200, "Đăng nhập Customer thất bại");
    customerToken = userRes.body.token;
  });

  test("TC-ADM-01: [Security RBAC] Khách hàng truy cập Dashboard Admin -> HTTP 403 Forbidden", async () => {
    const res = await request(app)
      .get("/api/dashboard")
      .set("Authorization", "Bearer " + customerToken);
    assert.equal(res.status, 403);
    assert.ok(res.body.message.includes("không có quyền"));
  });

  test("TC-ADM-02: [Positive] Admin truy cập Dashboard -> HTTP 200 & Đủ dữ liệu thống kê", async () => {
    const res = await request(app)
      .get("/api/dashboard")
      .set("Authorization", "Bearer " + adminToken);
    assert.equal(res.status, 200);
    assert.ok(typeof res.body.totalRecords === "number");
    assert.ok(typeof res.body.totalDoctors === "number");
    assert.ok(typeof res.body.todayAppointments === "number");
    assert.ok(typeof res.body.newContacts === "number");
    // Kiểm tra tính tương thích ngược cho Homestay aliases
    assert.equal(res.body.totalGuests, res.body.totalRecords);
    assert.equal(res.body.totalRooms, res.body.totalDoctors);
  });

  test("TC-ADM-03: [Positive] Admin lấy danh sách 30 ngày biểu đồ -> HTTP 200 & 30 phần tử", async () => {
    const res = await request(app)
      .get("/api/dashboard/daily-appointments")
      .set("Authorization", "Bearer " + adminToken);
    assert.equal(res.status, 200);
    assert.ok(Array.isArray(res.body));
    assert.equal(res.body.length, 30);
    assert.ok(res.body[0].date && typeof res.body[0].count === "number");
  });

  test("TC-ADM-04: [Positive] Admin lấy danh sách nhật ký hoạt động -> HTTP 200", async () => {
    const res = await request(app)
      .get("/api/hoatdong")
      .set("Authorization", "Bearer " + adminToken);
    assert.equal(res.status, 200);
    assert.ok(Array.isArray(res.body));
  });

  test("TC-ADM-05: [Positive] Admin thêm Loại hình Homestay mới -> HTTP 200", async () => {
    const uniqueName = "Loại Phòng Thử Nghiệm " + Date.now();
    const res = await request(app)
      .post("/api/loai-phong")
      .set("Authorization", "Bearer " + adminToken)
      .send({
        tenLoaiPhong: uniqueName,
      });
    assert.equal(res.status, 200);
    assert.equal(res.body.success, true);
    assert.ok(res.body.id);
    createdCategoryId = res.body.id;
  });

  test("TC-ADM-06: [Positive] Admin cập nhật Loại hình Homestay -> HTTP 200", async () => {
    assert.ok(createdCategoryId, "Chưa có ID loại hình để update");
    const updatedName = "Loại Phòng Đã Đổi Tên " + Date.now();
    const res = await request(app)
      .put("/api/loai-phong/" + createdCategoryId)
      .set("Authorization", "Bearer " + adminToken)
      .send({
        tenLoaiPhong: updatedName,
      });
    assert.equal(res.status, 200);
    assert.equal(res.body.success, true);
  });

  test("TC-ADM-07: [Positive] Admin xóa Loại hình Homestay thử nghiệm -> HTTP 200", async () => {
    assert.ok(createdCategoryId, "Chưa có ID loại hình để delete");
    const res = await request(app)
      .delete("/api/loai-phong/" + createdCategoryId)
      .set("Authorization", "Bearer " + adminToken);
    assert.equal(res.status, 200);
    assert.equal(res.body.success, true);
  });

  test("TC-ADM-08: [Positive] Admin xem tất cả đơn đặt homestay -> HTTP 200", async () => {
    const res = await request(app)
      .get("/api/admin/datphong")
      .set("Authorization", "Bearer " + adminToken);
    assert.equal(res.status, 200);
    assert.ok(Array.isArray(res.body));
  });
});
