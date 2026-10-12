// admin-lichkham.js
// Quản lý Đặt Homestay (Bookings) StayEasy
// Tự động gửi token xác thực cho các API quản trị.
(function() {
  if (window.__authFetchInstalled) return;
  window.__authFetchInstalled = true;
  const originalFetch = window.fetch.bind(window);
  window.fetch = function(url, options = {}) {
    const token = localStorage.getItem("token");
    if (token) {
      const headers = new Headers(options.headers || {});
      headers.set("Authorization", "Bearer " + token);
      options.headers = headers;
    }
    return originalFetch(url, options);
  };
})();

document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.querySelector("#lichTable tbody");
  if (!tableBody) return;

  const apiUrl = "http://localhost:3000/api/admin/lichkham";

  const modal = document.getElementById("lichModal");
  const openBtn = document.getElementById("openAddLich");
  const closeBtn = document.getElementById("closeLichModal");
  const cancelBtn = document.getElementById("cancelLich");
  const form = document.getElementById("lichForm");

  const idKHInput = document.getElementById("idKH");
  const hoTen = document.getElementById("hoTen");
  const lyDo = document.getElementById("lyDo");
  const ngayKham = document.getElementById("ngayKham");
  const gioKham = document.getElementById("gioKham");
  const idKhoa = document.getElementById("idKhoa");
  const idBacSi = document.getElementById("idBacSi");

  function escapeHtml(text) {
    if (text === null || text === undefined) return "";
    return String(text).replace(/[&<>"']/g, m => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;"
    }[m]));
  }

  // 🧾 Load danh sách đặt homestay
  async function loadAppointments() {
    if (!tableBody) return;
    tableBody.innerHTML = '<tr><td colspan="10" class="p-3 text-gray-500 text-center">Đang tải danh sách đặt homestay...</td></tr>';

    try {
      const res = await fetch(apiUrl);
      if (!res.ok) {
        if (res.status === 401 || res.status === 403) {
          throw new Error("UNAUTHORIZED");
        }
        throw new Error(`HTTP ${res.status}`);
      }
      const payload = await res.json();
      const data = Array.isArray(payload) ? payload : (payload?.data || []);

      tableBody.innerHTML = "";
      if (!Array.isArray(data) || data.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="10" class="p-3 text-gray-500 text-center">Không có đơn đặt homestay nào</td></tr>';
        return;
      }

      data.forEach((row) => {
        const tr = document.createElement("tr");
        tr.classList.add("border-t", "hover:bg-slate-50", "transition");
        const status = String(row.trangThai || "").toLowerCase();
        tr.innerHTML = `
          <td class="p-3 font-semibold text-slate-700">${escapeHtml(row.idLichKham)}</td>
          <td class="p-3">${escapeHtml(row.idKH || "-")}</td>
          <td class="p-3 font-medium text-slate-800">${escapeHtml(row.hoTen)}</td>
          <td class="p-3 text-slate-600 text-sm">${escapeHtml(row.lyDo || "Không có")}</td>
          <td class="p-3 font-medium text-blue-700">${escapeHtml(row.ngayKham)}</td>
          <td class="p-3">${escapeHtml(String(row.gioKham || "").slice(0, 5))}</td>
          <td class="p-3 font-semibold text-amber-700">${escapeHtml(row.tenBacSi)}</td>
          <td class="p-3">${escapeHtml(row.tenKhoa)}</td>
          <td class="p-3">
            <select data-id="${escapeHtml(row.idLichKham)}" class="border border-slate-300 rounded px-2 py-1 text-xs font-medium outline-none focus:ring-1 focus:ring-blue-500 ${status === 'đã xác nhận' ? 'bg-emerald-50 text-emerald-700 border-emerald-300' : (status === 'đã hủy' ? 'bg-rose-50 text-rose-700 border-rose-300' : 'bg-amber-50 text-amber-700 border-amber-300')}">
              <option value="chờ xác nhận" ${status === "chờ xác nhận" ? "selected" : ""}>chờ xác nhận</option>
              <option value="đã xác nhận" ${status === "đã xác nhận" ? "selected" : ""}>đã xác nhận</option>
              <option value="đã nhận phòng" ${status === "đã nhận phòng" ? "selected" : ""}>đã nhận phòng</option>
              <option value="đã hoàn thành" ${status === "đã hoàn thành" ? "selected" : ""}>đã hoàn thành</option>
              <option value="đã hủy" ${status === "đã hủy" ? "selected" : ""}>đã hủy</option>
            </select>
          </td>
          <td class="p-3 text-center">
            <button data-id="${escapeHtml(row.idLichKham)}" class="delBtn text-red-600 hover:text-red-800 transition">🗑️</button>
          </td>
        `;
        tableBody.appendChild(tr);
      });
    } catch (err) {
      console.error("❌ Lỗi tải đặt homestay:", err);
      if (String(err.message).includes("UNAUTHORIZED")) {
        window.location.href = "../Khách hàng/trangchupre/trangchu1.html";
        return;
      }
      tableBody.innerHTML = '<tr><td colspan="10" class="p-3 text-red-600 text-center">Không thể tải dữ liệu đặt homestay. Vui lòng kiểm tra quyền admin.</td></tr>';
    }
  }

  // 📘 Load danh sách loại hình homestay + căn
  async function loadOptions() {
    try {
      const khoaRes = await fetch("http://localhost:3000/api/khoa");
      if (!khoaRes.ok) throw new Error(`HTTP ${khoaRes.status}`);
      const khoaData = await khoaRes.json();
      idKhoa.innerHTML = '<option value="">-- Chọn loại hình homestay --</option>';
      (Array.isArray(khoaData) ? khoaData : []).forEach((k) =>
        idKhoa.innerHTML += `<option value="${escapeHtml(k.idKhoa)}">${escapeHtml(k.tenKhoa)}</option>`
      );

      idKhoa.addEventListener("change", async () => {
        const id = idKhoa.value;
        if (!id) return;
        try {
          const res = await fetch(`http://localhost:3000/api/bacsi/${id}`);
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          const data = await res.json();
          idBacSi.innerHTML = '<option value="">-- Chọn căn / phòng homestay --</option>';
          (Array.isArray(data) ? data : []).forEach((b) =>
            idBacSi.innerHTML += `<option value="${escapeHtml(b.idBacSi)}">${escapeHtml(b.hoTenBacSi)} (${escapeHtml(b.hocVi)})</option>`
          );
        } catch (err) {
          console.error("❌ Lỗi tải căn homestay:", err);
          idBacSi.innerHTML = '<option value="">-- Không tải được căn homestay --</option>';
        }
      });
    } catch (err) {
      console.error("❌ Lỗi tải loại hình homestay:", err);
      idKhoa.innerHTML = '<option value="">-- Không tải được loại hình homestay --</option>';
    }
  }

  // ✏️ Cập nhật trạng thái đặt phòng
  tableBody.addEventListener("change", async (e) => {
    if (e.target.tagName === "SELECT") {
      const id = e.target.dataset.id;
      const trangThai = e.target.value;
      await fetch(`${apiUrl}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ trangThai }),
      });
      loadAppointments();
    }
  });

  // 🗑️ Xóa đơn đặt homestay
  tableBody.addEventListener("click", async (e) => {
    if (e.target.classList.contains("delBtn")) {
      const id = e.target.dataset.id;
      if (confirm(`Bạn có chắc muốn xóa đơn đặt homestay #${id} này không?`)) {
        await fetch(`${apiUrl}/${id}`, { method: "DELETE" });
        loadAppointments();
      }
    }
  });

  // ➕ Mở modal thêm đơn đặt
  if (openBtn && modal && form) {
    openBtn.addEventListener("click", () => {
      modal.classList.remove("hidden");
      form.reset();
    });
  }
  if (closeBtn && modal) closeBtn.addEventListener("click", () => modal.classList.add("hidden"));
  if (cancelBtn && modal) cancelBtn.addEventListener("click", () => modal.classList.add("hidden"));

  // 🧩 Thêm đơn đặt homestay
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const idKH = idKHInput.value.trim();
    const hoTenVal = hoTen.value.trim();
    const lyDoVal = lyDo.value.trim();
    const ngayKhamVal = ngayKham.value;
    const gioKhamVal = gioKham.value;
    const idBacSiVal = idBacSi.value;
    const idKhoaVal = idKhoa.value;

    if (!idKH || !hoTenVal || !ngayKhamVal || !gioKhamVal || !idBacSiVal || !idKhoaVal) {
      return alert("⚠️ Vui lòng nhập đầy đủ thông tin đặt homestay!");
    }

    try {
      const checkKH = await fetch(`http://localhost:3000/api/admin/khachhang/${idKH}`);
      if (!checkKH.ok) throw new Error(`HTTP ${checkKH.status}`);
      const khData = await checkKH.json();

      if (!khData.exists) {
        return alert("❌ ID khách hàng không tồn tại trong hệ thống!");
      }

      const res = await fetch("http://localhost:3000/api/admin/lichkham", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          idKH,
          hoTen: hoTenVal,
          lyDo: lyDoVal,
          ngayKham: ngayKhamVal,
          gioKham: gioKhamVal,
          idBacSi: idBacSiVal,
          idKhoa: idKhoaVal,
        }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const result = await res.json();
      alert(result.message || "Tạo đơn đặt homestay thành công");
      modal.classList.add("hidden");
      loadAppointments();
    } catch (err) {
      console.error("❌ Lỗi thêm đơn đặt homestay:", err);
      alert("Không thể thêm đơn đặt homestay. Vui lòng kiểm tra server hoặc quyền admin.");
    }
  });

  loadAppointments();
  loadOptions();
});
