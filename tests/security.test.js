const { test, describe } = require("node:test");
const assert = require("node:assert/strict");
const request = require("supertest");
const { app } = require("../server.js");

describe("Security Hardening & Vulnerability Verification (IEEE 829 Test Suite)", () => {
  test("TC-SEC-01: [Security Headers] Kiểm tra sự hiện diện của các header phòng thủ", async () => {
    const res = await request(app).get("/health");
    assert.equal(res.headers["x-content-type-options"], "nosniff");
    assert.equal(res.headers["x-frame-options"], "DENY");
    assert.ok(res.headers["content-security-policy"]);
    assert.equal(res.headers["referrer-policy"], "no-referrer-when-downgrade");
  });

  test("TC-SEC-02: [CORS Whitelist] Cho phép Origin hợp lệ trong Whitelist", async () => {
    const res = await request(app)
      .get("/health")
      .set("Origin", "http://localhost:3000");
    assert.equal(res.headers["access-control-allow-origin"], "http://localhost:3000");
  });

  test("TC-SEC-03: [CORS Sandbox Defense] Từ chối Origin 'null' (CWE-942 Defense)", async () => {
    const res = await request(app)
      .get("/health")
      .set("Origin", "null");
    // Origin null không được trả về trong Access-Control-Allow-Origin
    assert.notEqual(res.headers["access-control-allow-origin"], "null");
  });

  test("TC-SEC-04: [CORS Untrusted Domain] Từ chối Origin lạ từ bên ngoài", async () => {
    const res = await request(app)
      .get("/health")
      .set("Origin", "http://hacker-phishing-site.xyz");
    assert.notEqual(res.headers["access-control-allow-origin"], "http://hacker-phishing-site.xyz");
  });

  test("TC-SEC-05: [Token Tampering] Token bị sửa đổi signature -> HTTP 403 Forbidden", async () => {
    // Lấy token thật từ login
    const loginRes = await request(app).post("/login").send({
      sdt: "0912345678",
      matkhau: "User@1234",
    });
    const validToken = loginRes.body.token;
    assert.ok(validToken);

    // Giả mạo phần chữ ký
    const parts = validToken.split(".");
    const tamperedToken = parts[0] + "." + parts[1] + ".FakeSignatureHere123";

    const res = await request(app)
      .get("/api/don-dat-user/1")
      .set("Authorization", "Bearer " + tamperedToken);
    assert.equal(res.status, 403);
    assert.ok(res.body.message.includes("Token xác thực không hợp lệ"));
  });

  test("TC-SEC-06: [Stored XSS Defense] Dữ liệu đầu vào chứa thẻ script được escape an toàn", async () => {
    const randomPhone = "09" + Math.floor(10000000 + Math.random() * 90000000);
    const xssPayload = "<script>alert('XSS_ATTACK')</script>";

    const regRes = await request(app).post("/register").send({
      hoten: xssPayload,
      sdt: randomPhone,
      matkhau: "UserPass@123",
    });
    assert.equal(regRes.status, 200);

    // Đăng nhập lấy token
    const loginRes = await request(app).post("/login").send({
      sdt: randomPhone,
      matkhau: "UserPass@123",
    });
    const userId = loginRes.body.user.idKH;
    const token = loginRes.body.token;

    // Xem thông tin cá nhân
    const userRes = await request(app)
      .get("/api/khachhang/" + userId)
      .set("Authorization", "Bearer " + token);
    assert.equal(userRes.status, 200);
    // Ký tự < và > phải được biến đổi thành thực thể an toàn &lt; và &gt;
    assert.ok(!userRes.body.hoTen.includes("<script>"));
    assert.ok(userRes.body.hoTen.includes("&lt;script&gt;"));
  });
});
