// admin-doctors.js
// Quản lý Danh sách Căn / Phòng Homestay StayEasy
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

const API_BASE_ADMIN = "http://localhost:3000/api/admin/bacsi";
const API_KHOA = "http://localhost:3000/api/khoa";

(async function initDoctorsModule(){
  const doctorsSection = document.querySelector('section[data-page="doctors"]');
  if (!doctorsSection) return;

  const table = doctorsSection.querySelector('table');
  if (!table) return;

  let tbody = table.querySelector('tbody');
  if (!tbody) {
    tbody = document.createElement('tbody');
    table.appendChild(tbody);
  }

  const existingAddBtn = doctorsSection.querySelector('button');

  const toolbar = document.createElement('div');
  toolbar.className = 'mb-4 flex items-center justify-between gap-3';
  toolbar.innerHTML = `
    <div class="flex items-center gap-2">
      <input id="doctorSearch" placeholder="🔍 Tìm tên căn hoặc loại hình homestay..." class="border rounded-lg px-3 py-2 text-sm w-72 outline-none focus:ring-2 focus:ring-blue-500" />
      <button id="refreshDoctors" class="px-3 py-2 border rounded-lg text-sm bg-white hover:bg-slate-50 transition">🔄 Làm mới</button>
    </div>
    <div></div>
  `;
  table.parentNode.insertBefore(toolbar, table);

  const searchInput = toolbar.querySelector('#doctorSearch');
  const refreshBtn = toolbar.querySelector('#refreshDoctors');

  if (existingAddBtn) {
    const addBtnClone = existingAddBtn.cloneNode(true);
    addBtnClone.id = 'addDoctorBtn';
    addBtnClone.textContent = '➕ Thêm căn mới';
    addBtnClone.className = 'bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition shadow-sm';
    toolbar.querySelector('div:last-child').appendChild(addBtnClone);
    existingAddBtn.style.display = 'none';
  } else {
    const addBtn = document.createElement('button');
    addBtn.id = 'addDoctorBtn';
    addBtn.className = 'bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition shadow-sm';
    addBtn.textContent = '➕ Thêm căn mới';
    toolbar.querySelector('div:last-child').appendChild(addBtn);
  }

  const addDoctorBtn = document.getElementById('addDoctorBtn');

  let doctors = [];
  let khoaList = [];

  async function loadKhoa() {
    try {
      const r = await fetch(API_KHOA);
      khoaList = await r.json();
    } catch (err) {
      console.error("Lỗi load loại hình homestay:", err);
      khoaList = [];
    }
  }

  async function loadDoctors(q = '') {
    try {
      const url = q ? `${API_BASE_ADMIN}?q=${encodeURIComponent(q)}` : API_BASE_ADMIN;
      const r = await fetch(url);
      doctors = await r.json();
      renderDoctors();
    } catch (err) {
      console.error("Lỗi load danh sách căn:", err);
      tbody.innerHTML = `<tr><td colspan="5" class="p-4 text-red-600 text-center">Lỗi khi tải danh sách căn homestay</td></tr>`;
    }
  }

  function renderDoctors() {
    if (!Array.isArray(doctors) || doctors.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" class="p-4 text-gray-500 text-center">Chưa có căn homestay nào</td></tr>`;
      return;
    }

    tbody.innerHTML = doctors.map(d => {
      const id = d.idBacSi || "";
      const name = escapeHtml(d.hoTenBacSi || d.tenBacSi || "");
      const hocVi = escapeHtml(d.hocVi || "");
      const tenKhoa = escapeHtml(d.tenKhoa || "");

      return `
        <tr class="border-t hover:bg-slate-50 transition">
          <td class="p-3 font-semibold text-slate-700">${id}</td>
          <td class="p-3 font-medium text-blue-700">${name}</td>
          <td class="p-3 text-slate-600">${hocVi}</td>
          <td class="p-3 font-medium text-slate-700">${tenKhoa}</td>
          <td class="p-3 text-center">
            <button class="editDoctor px-2 py-1 mr-2 text-blue-600 hover:text-blue-800 transition" data-id="${id}">✏️</button>
            <button class="deleteDoctor px-2 py-1 text-red-600 hover:text-red-800 transition" data-id="${id}">🗑️</button>
          </td>
        </tr>`;
    }).join("");

    tbody.querySelectorAll(".editDoctor").forEach(btn => {
      btn.addEventListener("click", () => openDoctorModal(btn.dataset.id));
    });
    tbody.querySelectorAll(".deleteDoctor").forEach(btn => {
      btn.addEventListener("click", () => deleteDoctor(btn.dataset.id));
    });
  }

  function openDoctorModal(id = null){
    const existing = id ? doctors.find(x => String(x.idBacSi) === String(id)) : null;

    const khoaOptions = khoaList.map(k => `<option value="${k.idKhoa}" ${existing && existing.idKhoa == k.idKhoa ? 'selected' : ''}>${escapeHtml(k.tenKhoa)}</option>`).join('');

    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 z-50 flex items-center justify-center bg-black/50';
    modal.innerHTML = `
      <div class="bg-white rounded-xl w-[92%] max-w-md p-6 shadow-2xl">
        <h3 class="text-lg font-bold mb-4 text-slate-800">${id ? 'Sửa thông tin căn homestay' : 'Thêm căn mới'}</h3>
        <form id="doctorForm" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1 text-slate-700">Tên căn / phòng homestay</label>
            <input name="hoTenBacSi" placeholder="VD: Bungalow 01 - Hoa Đậu Biếc" class="w-full border rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500" value="${escapeHtml(existing?.hoTenBacSi || '')}" required />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1 text-slate-700">Tiện nghi & Mức giá</label>
            <input name="hocVi" placeholder="VD: 1 Giường Queen, Bếp BBQ ngoài trời • 650.000đ/đêm" class="w-full border rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500" value="${escapeHtml(existing?.hocVi || '')}" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1 text-slate-700">Loại hình homestay</label>
            <select name="idKhoa" class="w-full border rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-blue-500" required>
              <option value="">-- Chọn loại hình homestay --</option>
              ${khoaOptions}
            </select>
          </div>
          <div class="flex justify-end gap-2 pt-3 border-t">
            <button type="button" id="cancelModal" class="px-4 py-2 border rounded-lg hover:bg-slate-100 transition">Hủy</button>
            <button type="submit" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition">${id ? 'Lưu thay đổi' : 'Thêm căn'}</button>
          </div>
        </form>
      </div>
    `;
    document.body.appendChild(modal);

    modal.querySelector('#cancelModal').addEventListener('click', ()=> modal.remove());
    modal.addEventListener('click', e => { if (e.target === modal) modal.remove(); });

    const form = modal.querySelector('#doctorForm');
    form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const fd = new FormData(form);
      const payload = Object.fromEntries(fd.entries());
      if (!payload.hoTenBacSi || !payload.idKhoa) {
        alert('Vui lòng điền tên căn và chọn loại hình homestay');
        return;
      }
      try {
        if (id) {
          const res = await fetch(`${API_BASE_ADMIN}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          const json = await res.json();
          if (!res.ok) throw new Error(json.message || 'Cập nhật thất bại');
          alert(json.message || 'Cập nhật thành công');
        } else {
          const res = await fetch(API_BASE_ADMIN, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          const json = await res.json();
          if (!res.ok) throw new Error(json.message || 'Thêm thất bại');
          alert(json.message || 'Thêm thành công');
        }
      } catch (err) {
        console.error(err);
        alert(err.message || 'Lỗi khi lưu thông tin căn homestay');
      } finally {
        modal.remove();
        await loadDoctors(searchInput.value.trim());
      }
    });
  }

  async function deleteDoctor(id) {
    if (!id) return;

    try {
      const res = await fetch(`${API_BASE_ADMIN}/${id}`, { method: "DELETE" });
      const result = await res.json();

      if (result.requireConfirm) {
        const confirmDelete = confirm(result.message + "\n\nChọn OK để xóa toàn bộ, Cancel để hủy.");
        if (confirmDelete) {
          const res2 = await fetch(`${API_BASE_ADMIN}/${id}?force=true`, { method: "DELETE" });
          const result2 = await res2.json();
          alert(result2.message || "🗑️ Đã xóa căn và toàn bộ dữ liệu liên quan!");
        } else {
          alert("❎ Đã hủy xóa.");
        }
      } else {
        alert(result.message || "🗑️ Đã xóa căn homestay thành công!");
      }

      await loadDoctors(searchInput.value.trim());
    } catch (err) {
      console.error("❌ Lỗi khi xóa căn:", err);
      alert("Đã xảy ra lỗi khi xóa căn homestay!");
    }
  }

  function escapeHtml(str){
    if (str == null) return '';
    return String(str).replace(/[&<>"']/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[m]);
  }

  addDoctorBtn.addEventListener('click', ()=> openDoctorModal());
  refreshBtn.addEventListener('click', ()=> loadDoctors(searchInput.value.trim()));
  searchInput.addEventListener('input', (e)=> {
    loadDoctors(e.target.value.trim());
  });

  await loadKhoa();
  await loadDoctors();
})();
