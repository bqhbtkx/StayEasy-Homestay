const { test, describe } = require("node:test");
const assert = require("node:assert/strict");
const request = require("supertest");
const { app } = require("../server.js");

describe("Authentication & User Lifecycle (IEEE 829 Test Suite)", () => {
  const uniquePhone = "09" + Math.floor(10000000 + Math.random() * 90000000);
  const validPassword = "UserPass@123";

  test("TC-AUTH-01: [Negative] Đăng ký thiếu trường bắt buộc -> HTTP 400", async () => {
    const res = await request(app).post("/register").send({
      hoten: "Nguyễn Văn Test",
      sdt: uniquePhone,
      // missing matkhau
    });
    assert.equal(res.status, 400);
    assert.ok(res.body.message.includes("Vui lòng nhập đầy đủ"));
  });

  test("TC-AUTH-02: [Negative] Đăng ký với mật khẩu yếu (< 8 ký tự hoặc thiếu chữ/số) -> HTTP 400", async () => {
    const res = await request(app).post("/register").send({
      hoten: "Nguyễn Văn Test",
      sdt: uniquePhone,
      matkhau: "12345",
    });
    assert.equal(res.status, 400);
    assert.ok(res.body.message.includes("ít nhất 8 ký tự"));
  });

  test("TC-AUTH-03: [Negative] Đăng ký với số điện thoại sai định dạng -> HTTP 400", async () => {
    const res = await request(app).post("/register").send({
      hoten: "Nguyễn Văn Test",
      sdt: "abc123456",
      matkhau: validPassword,
    });
    assert.equal(res.status, 400);
    assert.ok(res.body.message.includes("Số điện thoại không hợp lệ"));
  });

  test("TC-AUTH-04: [Positive] Đăng ký tài khoản hợp lệ -> HTTP 200", async () => {
    const res = await request(app).post("/register").send({
      hoten: "Nguyễn Văn Hợp Lệ",
      sdt: uniquePhone,
      matkhau: validPassword,
    });
    assert.equal(res.status, 200);
    assert.ok(res.body.message.includes("Đăng ký thành công"));
  });

  test("TC-AUTH-05: [Negative] Đăng ký trùng số điện thoại đã tồn tại -> HTTP 400", async () => {
    const res = await request(app).post("/register").send({
      hoten: "Người Trùng SĐT",
      sdt: uniquePhone,
      matkhau: validPassword,
    });
    assert.equal(res.status, 400);
    assert.ok(res.body.message.includes("đã được đăng ký"));
  });

  test("TC-AUTH-06: [Negative] Đăng nhập sai mật khẩu -> HTTP 401", async () => {
    const res = await request(app).post("/login").send({
      sdt: uniquePhone,
      matkhau: "WrongPassword999",
    });
    assert.equal(res.status, 401);
    assert.ok(res.body.message.includes("không đúng"));
  });

  test("TC-AUTH-07: [Positive] Đăng nhập tài khoản khách hàng hợp lệ -> HTTP 200 & Trả Token", async () => {
    const res = await request(app).post("/login").send({
      sdt: uniquePhone,
      matkhau: validPassword,
    });
    assert.equal(res.status, 200);
    assert.equal(res.body.isAdmin, false);
    assert.ok(typeof res.body.token === "string" && res.body.token.split(".").length === 3);
    assert.equal(res.body.user.sdt, uniquePhone);
  });

  test("TC-AUTH-08: [Positive] Đăng nhập tài khoản Admin mặc định -> HTTP 200 & Role Admin", async () => {
    const res = await request(app).post("/login").send({
      sdt: "0900000000",
      matkhau: "Admin@123",
    });
    assert.equal(res.status, 200);
    assert.equal(res.body.isAdmin, true);
    assert.ok(typeof res.body.token === "string" && res.body.token.split(".").length === 3);
    assert.equal(res.body.admin.sdt, "0900000000");
  });
});
