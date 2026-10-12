// admin-lskhambenh.js
// Quản lý Lịch sử lưu trú & Hóa đơn kỳ nghỉ StayEasy Homestay
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
  const tableBody = document.querySelector("#lichsuTable tbody");
  if (!tableBody) return;

  const modal = document.getElementById("lichsuModal");
  const openBtn = document.getElementById("openAddLS");
  const closeBtn = document.getElementById("closeLSModal");
  const cancelBtn = document.getElementById("cancelLS");
  const form = document.getElementById("lichsuForm");
  const apiUrl = "http://localhost:3000/api/admin/lichsu";

  const idBacSiEl = document.getElementById("idBacSiLS");
  const idKhoaEl = document.getElementById("idKhoaLS");
  const idHSEl = document.getElementById("idHoSoYTeLS");

  function safeText(str) {
    if (str === null || str === undefined) return "";
    return String(str).replace(/[&<>"']/g, m => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;"
    }[m]));
  }

  // load danh sách phòng theo loại phòng
  async function loadBacSiTheoKhoa(idKhoaValue, selectValue = null) {
    try {
      if (!idKhoaValue) {
        idBacSiEl.innerHTML = `<option value="">-- Chọn căn / phòng homestay --</option>`;
        return;
      }
      const res = await fetch(`http://localhost:3000/api/bacsi/khoa/${idKhoaValue}`);
      if (!res.ok) throw new Error("Không lấy được danh sách căn");
      const bacsi = await res.json();
      if (!Array.isArray(bacsi) || bacsi.length === 0) {
        idBacSiEl.innerHTML = `<option value="">(Không có căn thuộc loại này)</option>`;
        return;
      }
      idBacSiEl.innerHTML = bacsi
        .map(b => `<option value="${b.idBacSi}">${safeText(b.hoTenBacSi)}</option>`)
        .join("");
      if (selectValue) idBacSiEl.value = selectValue;
    } catch (err) {
      console.error("❌ loadBacSiTheoKhoa:", err);
      idBacSiEl.innerHTML = `<option value="">(Lỗi tải căn homestay)</option>`;
    }
  }

  // load options (loại phòng + hồ sơ)
  async function loadOptions(defaultKhoaId = null, selectedBacSi = null, selectedHS = null) {
    try {
      const [khoaRes, hsRes] = await Promise.all([
        fetch("http://localhost:3000/api/khoa"),
        fetch("http://localhost:3000/api/admin/hosoyte")
      ]);

      if (!khoaRes.ok) throw new Error("Lỗi tải loại hình homestay");
      if (!hsRes.ok) throw new Error("Lỗi tải hồ sơ");

      const [khoa, hs] = await Promise.all([khoaRes.json(), hsRes.json()]);

      if (Array.isArray(khoa) && khoa.length) {
        idKhoaEl.innerHTML = `<option value="">-- Chọn loại hình homestay --</option>` +
          khoa.map(k => `<option value="${k.idKhoa}">${safeText(k.tenKhoa)}</option>`).join("");
        if (defaultKhoaId) idKhoaEl.value = defaultKhoaId;
      } else {
        idKhoaEl.innerHTML = `<option value="">(Không có loại hình homestay)</option>`;
      }

      if (Array.isArray(hs) && hs.length) {
        idHSEl.innerHTML = `<option value="">-- Chọn mã hồ sơ khách --</option>` +
          hs.map(h => `<option value="${h.idHoSoYTe}">SE-HOME${String(h.idHoSoYTe).padStart(4, '0')} (Mã KH: ${h.idKH || ""})</option>`).join("");
        if (selectedHS) idHSEl.value = selectedHS;
      } else {
        idHSEl.innerHTML = `<option value="">(Không có hồ sơ khách)</option>`;
      }

      const targetKhoa = defaultKhoaId || (Array.isArray(khoa) && khoa.length ? khoa[0].idKhoa : null);
      await loadBacSiTheoKhoa(targetKhoa, selectedBacSi);
    } catch (err) {
      console.error("❌ loadOptions:", err);
      idKhoaEl.innerHTML = `<option value="">(Lỗi tải loại hình homestay)</option>`;
      idHSEl.innerHTML = `<option value="">(Lỗi tải hồ sơ)</option>`;
      idBacSiEl.innerHTML = `<option value="">(Lỗi tải căn homestay)</option>`;
    }
  }

  async function loadData() {
    try {
      const res = await fetch(apiUrl);
      if (!res.ok) {
        if (res.status === 401 || res.status === 403) {
          throw new Error("UNAUTHORIZED");
        }
        throw new Error("Lỗi lấy dữ liệu lịch sử");
      }
      const data = await res.json();
      tableBody.innerHTML = "";
      if (!Array.isArray(data) || data.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="8" class="p-3 text-gray-500 text-center">Chưa có lịch sử lưu trú nào</td></tr>';
        return;
      }

      data.forEach(row => {
        const tr = document.createElement("tr");
        tr.classList.add("border-t", "hover:bg-slate-50", "transition");
        const ngay = safeText(row.ngayKham).includes("T") ? row.ngayKham.split("T")[0] : safeText(row.ngayKham);
        tr.innerHTML = `
          <td class="p-3 font-semibold text-slate-700">${row.idLS}</td>
          <td class="p-3 font-medium text-blue-700">${ngay}</td>
          <td class="p-3 font-medium text-emerald-700">${safeText(row.ketLuan)}</td>
          <td class="p-3 text-slate-600 text-sm">${safeText(row.chiTiet)}</td>
          <td class="p-3 font-semibold text-amber-700">${safeText(row.tenBacSi || "")}</td>
          <td class="p-3">${safeText(row.tenKhoa || "")}</td>
          <td class="p-3 text-slate-500">SE-HOME${String(row.idHoSoYTe || "").padStart(4, '0')}</td>
          <td class="p-3 text-center">
            <button class="editBtn text-blue-600 hover:text-blue-800 mr-2 transition" data-id="${row.idLS}">✏️ Sửa</button>
            <button class="delBtn text-red-600 hover:text-red-800 transition" data-id="${row.idLS}">🗑️ Xóa</button>
          </td>
        `;
        tableBody.appendChild(tr);
      });
    } catch (err) {
      console.error("❌ loadData:", err);
      if (String(err.message).includes("UNAUTHORIZED")) {
        window.location.href = "../Khách hàng/trangchupre/trangchu1.html";
        return;
      }
      tableBody.innerHTML = `<tr><td colspan="8" class="p-4 text-red-600 text-center">Lỗi tải dữ liệu lịch sử lưu trú</td></tr>`;
    }
  }

  tableBody.addEventListener("click", async (e) => {
    const btn = e.target.closest(".delBtn");
    if (!btn) return;
    const id = btn.dataset.id;
    if (!confirm("Bạn có chắc muốn xóa bản ghi lịch sử lưu trú này?")) return;
    try {
      const res = await fetch(`${apiUrl}/${id}`, { method: "DELETE" });
      const result = await res.json();
      alert(result.message || "Đã xóa thành công");
      await loadData();
    } catch (err) {
      console.error("❌ Xóa lỗi:", err);
      alert("Xảy ra lỗi khi xóa");
    }
  });

  tableBody.addEventListener("click", async (e) => {
    const btn = e.target.closest(".editBtn");
    if (!btn) return;
    const id = btn.dataset.id;
    try {
      let record = null;
      try {
        const oneRes = await fetch(`${apiUrl}/${id}`);
        if (oneRes.ok) record = await oneRes.json();
      } catch (_) {
        const allRes = await fetch(apiUrl);
        const all = await allRes.json();
        record = all.find(r => String(r.idLS) === String(id));
      }
      if (!record) return alert("Không tìm thấy bản ghi để sửa");

      document.getElementById("lichsuTitle").innerText = "Sửa lịch sử lưu trú";
      document.getElementById("idLS").value = record.idLS;
      const ngayVal = safeText(record.ngayKham).includes("T") ? record.ngayKham.split("T")[0] : record.ngayKham;
      document.getElementById("ngayKhamLS").value = ngayVal || "";
      document.getElementById("ketLuanLS").value = record.ketLuan || "";
      document.getElementById("chiTietLS").value = record.chiTiet || "";

      const defaultKhoaId = record.idKhoa || null;
      const defaultBacSiId = record.idBacSi || null;
      const defaultHS = record.idHoSoYTe || null;

      await loadOptions(defaultKhoaId, defaultBacSiId, defaultHS);

      if (!defaultBacSiId && record.tenBacSi) {
        const opt = Array.from(idBacSiEl.options).find(o => o.textContent.trim() === record.tenBacSi.trim());
        if (opt) idBacSiEl.value = opt.value;
      }
      if (!defaultKhoaId && record.tenKhoa) {
        const opt2 = Array.from(idKhoaEl.options).find(o => o.textContent.trim() === record.tenKhoa.trim());
        if (opt2) {
          idKhoaEl.value = opt2.value;
          await loadBacSiTheoKhoa(idKhoaEl.value, defaultBacSiId);
        }
      }

      modal.classList.remove("hidden");
    } catch (err) {
      console.error("❌ Sửa lỗi:", err);
      alert("Lỗi khi mở form sửa");
    }
  });

  if (openBtn && modal && form) {
    openBtn.addEventListener("click", async () => {
      form.reset();
      document.getElementById("lichsuTitle").innerText = "Thêm lịch sử lưu trú";
      document.getElementById("idLS").value = "";
      await loadOptions();
      modal.classList.remove("hidden");
    });
  }

  if (closeBtn && modal) closeBtn.addEventListener("click", () => modal.classList.add("hidden"));
  if (cancelBtn && modal) cancelBtn.addEventListener("click", () => modal.classList.add("hidden"));

  if (form && modal) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const id = document.getElementById("idLS").value;
      const payload = {
        ngayKham: document.getElementById("ngayKhamLS").value,
        ketLuan: document.getElementById("ketLuanLS").value.trim(),
        chiTiet: document.getElementById("chiTietLS").value.trim(),
        idBacSi: document.getElementById("idBacSiLS").value,
        idKhoa: document.getElementById("idKhoaLS").value,
        idHoSoYTe: document.getElementById("idHoSoYTeLS").value
      };

      if (!payload.ngayKham || !payload.ketLuan || !payload.idBacSi || !payload.idKhoa || !payload.idHoSoYTe) {
        return alert("Vui lòng nhập đầy đủ thông tin bắt buộc (ngày check-out, đánh giá, phòng nghỉ, loại phòng, mã hồ sơ).");
      }

      try {
        const method = id ? "PUT" : "POST";
        const url = id ? `${apiUrl}/${id}` : apiUrl;
        const res = await fetch(url, {
          method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const result = await res.json();
        alert(result.message || (id ? "Đã cập nhật kỳ nghỉ thành công" : "Đã thêm kỳ nghỉ thành công"));
        modal.classList.add("hidden");
        await loadData();
      } catch (err) {
        console.error("❌ Lưu lỗi:", err);
        alert("Lỗi khi lưu dữ liệu");
      }
    });
  }

  if (idKhoaEl) {
    idKhoaEl.addEventListener("change", (e) => {
      const v = e.target.value;
      loadBacSiTheoKhoa(v);
    });
  }

  loadData();
});
