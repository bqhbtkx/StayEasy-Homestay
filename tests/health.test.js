const { test, describe, after } = require("node:test");
const assert = require("node:assert/strict");
const request = require("supertest");
const { app, db } = require("../server.js");

describe("API Health & System Verification", () => {
  after(() => {
    // Database connection pool can remain open or close cleanly
  });

  test("GET /health should return 200 with healthy status and database connected", async () => {
    const res = await request(app).get("/health");
    assert.equal(res.status, 200);
    assert.equal(res.body.status, "healthy");
    assert.equal(res.body.database, "connected");
    assert.equal(res.body.service, "StayEasy Homestay API");
    assert.ok(typeof res.body.uptime === "number");
    assert.ok(res.body.timestamp);
  });

  test("GET /api/health alias should also return 200 with identical structure", async () => {
    const res = await request(app).get("/api/health");
    assert.equal(res.status, 200);
    assert.equal(res.body.status, "healthy");
    assert.equal(res.body.database, "connected");
  });

  test("GET /api/nonexistent-endpoint should return 404 with standard JSON message", async () => {
    const res = await request(app).get("/api/unknown-service-path");
    assert.equal(res.status, 404);
    assert.ok(res.body.message.includes("API endpoint không tồn tại"));
  });
});
