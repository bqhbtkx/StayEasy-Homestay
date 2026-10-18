// admin-loaiphong.js
// Quản lý Loại hình Homestay StayEasy
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
  const API = "http://localhost:3000/api/loai-phong";
  const tableBody = document.querySelector("#deptTable tbody");
  if (!tableBody) return;

  const openAddBtn = document.getElementById("openAddDept");
  const refreshBtn = document.getElementById("refreshDept");

  const modal = document.getElementById("deptModal");
  const form = document.getElementById("deptForm");
  const idInput = document.getElementById("deptIdKhoa");
  const nameInput = document.getElementById("tenKhoa");
  const title = document.getElementById("deptModalTitle");
  const closeBtn = document.getElementById("closeDeptModal");
  const cancelBtn = document.getElementById("cancelDept");

  function escapeHtml(str) {
    return str ? str.replace(/[&<>"']/g, m => ({ "&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;" }[m])) : "";
  }

  // 📋 Load danh sách loại hình homestay
  async function loadData() {
    tableBody.innerHTML = `<tr><td colspan="3" class="p-3 text-gray-500 text-center">Đang tải danh sách...</td></tr>`;
    try {
      const res = await fetch(API);
      const data = await res.json();
      tableBody.innerHTML = "";
      if (!Array.isArray(data) || !data.length) {
        tableBody.innerHTML = `<tr><td colspan="3" class="p-3 text-gray-500 text-center">Chưa có loại hình homestay nào</td></tr>`;
        return;
      }
      data.forEach((khoa) => {
        const tr = document.createElement("tr");
        tr.classList.add("border-t", "hover:bg-slate-50", "transition");
        tr.innerHTML = `
          <td class="p-3 font-semibold text-slate-700">${escapeHtml(String(khoa.idKhoa))}</td>
          <td class="p-3 font-medium text-blue-700">${escapeHtml(khoa.tenKhoa)}</td>
          <td class="p-3 text-center">
            <button class="editBtn text-blue-600 hover:text-blue-800 mr-3 transition" data-id="${khoa.idKhoa}" data-name="${encodeURIComponent(khoa.tenKhoa)}">✏️ Sửa</button>
            <button class="delBtn text-red-600 hover:text-red-800 transition" data-id="${khoa.idKhoa}">🗑️ Xóa</button>
          </td>`;
        tableBody.appendChild(tr);
      });
    } catch (err) {
      console.error("❌ Lỗi tải danh sách loại hình:", err);
      tableBody.innerHTML = `<tr><td colspan="3" class="text-red-600 p-3 text-center">Lỗi tải dữ liệu</td></tr>`;
    }
  }

  // ➕ Mở modal thêm
  if (openAddBtn && form && modal && idInput && title) {
    openAddBtn.addEventListener("click", () => {
      form.reset();
      idInput.value = "";
      title.textContent = "Thêm loại hình homestay mới";
      modal.classList.remove("hidden");
    });
  }

  // 🧩 Đóng modal
  [closeBtn, cancelBtn].forEach((btn) => {
    if (btn && modal) btn.addEventListener("click", () => modal.classList.add("hidden"));
  });

  // 💾 Thêm / Sửa
  if (!form || !idInput || !nameInput || !modal) return;
  form.addEventListener("submit", async e => {
    e.preventDefault();
    const id = idInput.value;
    const tenKhoa = nameInput.value.trim();
    if (!tenKhoa) return alert("Tên loại hình homestay không được để trống!");

    try {
      const method = id ? "PUT" : "POST";
      const url = id ? `${API}/${id}` : API;
      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tenKhoa })
      });
      const data = await res.json();
      alert(data.message || (id ? "Cập nhật thành công" : "Thêm loại hình homestay thành công"));
      modal.classList.add("hidden");
      loadData();
    } catch (err) {
      console.error("❌ Lỗi lưu loại hình homestay:", err);
      alert("Lỗi khi lưu loại hình homestay");
    }
  });

  // ✏️ Sửa
  tableBody.addEventListener("click", e => {
    const editBtn = e.target.closest(".editBtn");
    if (!editBtn) return;
    idInput.value = editBtn.dataset.id;
    nameInput.value = decodeURIComponent(editBtn.dataset.name);
    title.textContent = "Sửa loại hình homestay";
    modal.classList.remove("hidden");
  });

  // 🗑️ Xóa
  tableBody.addEventListener("click", async e => {
    const delBtn = e.target.closest(".delBtn");
    if (!delBtn) return;
    const id = delBtn.dataset.id;
    if (!confirm("Bạn có chắc muốn xóa loại hình homestay này không?")) return;

    try {
      const res = await fetch(`${API}/${id}`, { method: "DELETE" });
      const result = await res.json();

      if (result.requireConfirm && Array.isArray(result.doctors)) {
        let msg = `${result.message}\n\nChi tiết căn homestay bị ảnh hưởng:\n`;
        result.doctors.forEach(b => {
          msg += `- ${b.hoTenBacSi} (Đơn đặt: ${b.lichCount}, Lịch sử: ${b.lichsuCount})\n`;
        });
        msg += "\nChọn OK để xóa toàn bộ, Cancel để hủy.";
        if (confirm(msg)) {
          const forceRes = await fetch(`${API}/${id}?force=true`, { method: "DELETE" });
          const j2 = await forceRes.json();
          alert(j2.message || "Đã xóa loại hình homestay và toàn bộ dữ liệu liên quan!");
        } else {
          alert("❎ Đã hủy thao tác xóa.");
        }
      } else {
        alert(result.message || "🗑️ Đã xóa loại hình homestay thành công!");
      }

      loadData();
    } catch (err) {
      console.error("❌ Lỗi xóa loại hình homestay:", err);
      alert("Lỗi khi xóa loại hình homestay");
    }
  });

  if (refreshBtn) refreshBtn.addEventListener("click", loadData);
  loadData();
});
