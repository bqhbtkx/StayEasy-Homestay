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

function adminLoginUrl() {
  const onApiHost = /:(3000)$/.test(location.host) || location.pathname.startsWith("/admin-panel");
  return onApiHost
    ? "/customer/trangchupre/trangchu1.html"
    : "../Khách hàng/trangchupre/trangchu1.html";
}

document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.querySelector("#hosoyteTable tbody");
  if (!tableBody) return;

  const apiUrl = "http://localhost:3000/api/admin/hosoluutru";
  const modal = document.getElementById("hosoyteModal");
  const closeBtn = document.getElementById("closeHosoyteModal");
  const cancelBtn = document.getElementById("cancelHosoyte");
  const addBtn = document.getElementById("openAddHosoyte");
  const form = document.getElementById("hosoyteForm");
  const idKHInput = document.getElementById("idKHInput");

  async function loadData() {
    tableBody.innerHTML = '<tr><td colspan="3" class="p-2 text-gray-500">Đang tải...</td></tr>';

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
        tableBody.innerHTML = '<tr><td colspan="3" class="p-3 text-gray-500 text-center">Không có hồ sơ khách lưu trú nào</td></tr>';
        return;
      }

      data.forEach((hs) => {
        const tr = document.createElement("tr");
        tr.classList.add("border-t", "hover:bg-slate-50", "transition");
        tr.innerHTML = `
          <td class="p-3 font-semibold text-slate-700">SE-HOME${String(hs.idHoSoYTe ?? "").padStart(4, '0')}</td>
          <td class="p-3 text-blue-700 font-medium">${hs.idKH ?? ""}</td>
          <td class="p-3 text-center">
            <button class="viewBtn text-blue-600 hover:text-blue-800 mr-2" data-id="${hs.idHoSoYTe ?? ""}">👁️ Xem</button>
            <button class="delBtn text-red-600 hover:text-red-800" data-id="${hs.idHoSoYTe ?? ""}">🗑️ Xóa</button>
          </td>
        `;
        tableBody.appendChild(tr);
      });
    } catch (err) {
      console.error("❌ Lỗi tải hồ sơ khách lưu trú:", err);
      if (String(err.message).includes("UNAUTHORIZED")) {
        window.location.href = adminLoginUrl();
        return;
      }
      tableBody.innerHTML = '<tr><td colspan="3" class="p-3 text-red-600 text-center">Không thể tải dữ liệu. Vui lòng kiểm tra quyền admin.</td></tr>';
    }
  }

  tableBody.addEventListener("click", async (e) => {
    const viewBtn = e.target.closest(".viewBtn");
    const delBtn = e.target.closest(".delBtn");

    if (viewBtn) {
      const id = viewBtn.dataset.id;
      try {
        const res = await fetch(`${apiUrl}/${id}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const hs = await res.json();
        alert(`📋 Thẻ Thành Viên StayEasy Homestay #${hs.idHoSoYTe}\n👤 Họ tên: ${hs.hoTen || "Chưa có"}\n🆔 Mã khách: ${hs.idKH}`);
      } catch (err) {
        console.error("❌ Lỗi xem hồ sơ:", err);
        alert("Không thể tải chi tiết hồ sơ. Vui lòng kiểm tra quyền admin.");
      }
      return;
    }

    if (delBtn) {
      const id = delBtn.dataset.id;
      if (!id) return;

      try {
        const res = await fetch(`${apiUrl}/${id}`, { method: "DELETE" });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const check = await res.json();

        if (check.requireConfirm) {
          const confirmDelete = confirm(check.message + "\n\nChọn OK để xóa toàn bộ, Cancel để hủy.");
          if (confirmDelete) {
            await fetch(`${apiUrl}/${id}?force=true`, { method: "DELETE" });
            alert("🗑️ Đã xóa hồ sơ cùng các lịch liên quan!");
          } else {
            alert("❎ Đã hủy xóa.");
          }
        } else {
          alert(check.message || "🗑️ Đã xóa hồ sơ khách lưu trú!");
        }
      } catch (err) {
        console.error("❌ Lỗi xóa hồ sơ:", err);
        alert("Không thể xóa hồ sơ. Vui lòng kiểm tra quyền admin.");
      }

      loadData();
    }
  });

  if (addBtn && modal && form) {
    addBtn.addEventListener("click", () => {
      modal.classList.remove("hidden");
      form.reset();
    });
  }
  if (closeBtn && modal) closeBtn.addEventListener("click", () => modal.classList.add("hidden"));
  if (cancelBtn && modal) cancelBtn.addEventListener("click", () => modal.classList.add("hidden"));

  if (form && idKHInput && modal) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const idKH = idKHInput.value.trim();
      if (!idKH) return alert("Vui lòng nhập ID khách hàng!");
      try {
        const res = await fetch(apiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ idKH }),
        });
        const result = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(result.message || `HTTP ${res.status}`);
        alert(result.message || "Thêm hồ sơ thành công");
        modal.classList.add("hidden");
        loadData();
      } catch (err) {
        console.error("❌ Lỗi thêm hồ sơ:", err);
        alert(err.message || "Không thể thêm hồ sơ. Vui lòng kiểm tra server hoặc quyền admin.");
      }
    });
  }

  loadData();
});
