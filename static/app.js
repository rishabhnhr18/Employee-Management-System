/* ── State ── */
let employees = [];
let filteredEmployees = [];
let sortState = { col: null, dir: "asc" };
let editingId = null;
let deleteTargetId = null;
let meta = { departments: [], roles: [], genders: [] };
let chartInstances = {};

const CHART_COLORS = [
  "#0C9295","#FF7F0E","#2CA02C","#D62728","#9467BD",
  "#8C564B","#E377C2","#7F7F7F","#BCBD22","#17BECF"
];

/* ── DOM refs ── */
const tbody        = document.getElementById("empTbody");
const searchInput  = document.getElementById("searchInput");
const rowCount     = document.getElementById("rowCount");
const modalOverlay = document.getElementById("modalOverlay");
const deleteOverlay= document.getElementById("deleteOverlay");
const empForm      = document.getElementById("empForm");
const modalTitle   = document.getElementById("modalTitle");
const submitBtn    = document.getElementById("submitBtn");
const idField      = document.getElementById("f-id");
const toast        = document.getElementById("toast");

/* ── Toast ── */
let toastTimer;
function showToast(msg, type = "success") {
  clearTimeout(toastTimer);
  toast.textContent = msg;
  toast.className = `toast ${type} show`;
  toastTimer = setTimeout(() => { toast.className = "toast"; }, 3200);
}

/* ── API helpers ── */
async function api(method, path, body) {
  const opts = { method, headers: { "Content-Type": "application/json" } };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(path, opts);
  const json = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(json.error || `HTTP ${res.status}`);
  return json;
}

/* ── Bootstrap ── */
async function init() {
  try {
    meta = await api("GET", "/api/meta");
    populateSelects();
    await refresh();
  } catch (e) {
    showToast("Failed to load data: " + e.message, "error");
  }
}

function populateSelects() {
  const fill = (id, items) => {
    const sel = document.getElementById(id);
    items.forEach(v => {
      const opt = document.createElement("option");
      opt.value = opt.textContent = v;
      sel.appendChild(opt);
    });
  };
  fill("f-dept",   meta.departments);
  fill("f-role",   meta.roles);
  fill("f-gender", meta.genders);
}

async function refresh() {
  const [emps, stats] = await Promise.all([
    api("GET", "/api/employees"),
    api("GET", "/api/stats"),
  ]);
  employees = emps;
  applyFilter();
  updateCards(stats);
  updateCharts(stats);
}

/* ── Cards ── */
function updateCards(stats) {
  document.getElementById("totalCount").textContent = stats.total;
  document.getElementById("deptCount").textContent  = Object.keys(stats.departments).length;
  document.getElementById("roleCount").textContent  = Object.keys(stats.roles).length;
  document.getElementById("genderCount").textContent= Object.keys(stats.genders).length;
}

/* ── Table ── */
function applyFilter() {
  const q = searchInput.value.toLowerCase().trim();
  filteredEmployees = q
    ? employees.filter(e =>
        e.id.toLowerCase().includes(q) ||
        e.name.toLowerCase().includes(q) ||
        e.department.toLowerCase().includes(q) ||
        e.role.toLowerCase().includes(q) ||
        e.gender.toLowerCase().includes(q))
    : [...employees];
  if (sortState.col) applySortToFiltered();
  renderTable();
}

function applySortToFiltered() {
  const { col, dir } = sortState;
  filteredEmployees.sort((a, b) => {
    const av = (a[col] || "").toString().toLowerCase();
    const bv = (b[col] || "").toString().toLowerCase();
    return dir === "asc" ? av.localeCompare(bv) : bv.localeCompare(av);
  });
}

function renderTable() {
  if (!filteredEmployees.length) {
    tbody.innerHTML = `<tr><td colspan="6" class="empty-row">No employees found</td></tr>`;
    rowCount.textContent = "0 employees";
    return;
  }
  tbody.innerHTML = filteredEmployees.map(e => `
    <tr>
      <td>${esc(e.id)}</td>
      <td>${esc(e.name)}</td>
      <td><span class="badge badge-dept">${esc(e.department)}</span></td>
      <td><span class="badge badge-role">${esc(e.role)}</span></td>
      <td><span class="badge badge-${e.gender.toLowerCase()}">${esc(e.gender)}</span></td>
      <td>
        <button class="btn-icon" title="Edit"   onclick="openEdit('${esc(e.id)}')">✏️</button>
        <button class="btn-icon" title="Delete" onclick="openDelete('${esc(e.id)}','${esc(e.name)}')">🗑️</button>
      </td>
    </tr>`).join("");
  rowCount.textContent = `${filteredEmployees.length} employee${filteredEmployees.length !== 1 ? "s" : ""}`;
}

function esc(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

/* ── Sorting ── */
document.querySelectorAll("th.sortable").forEach(th => {
  th.addEventListener("click", () => {
    const col = th.dataset.col;
    if (sortState.col === col) {
      sortState.dir = sortState.dir === "asc" ? "desc" : "asc";
    } else {
      sortState = { col, dir: "asc" };
    }
    document.querySelectorAll("th.sortable").forEach(t => t.classList.remove("sort-asc","sort-desc"));
    th.classList.add(sortState.dir === "asc" ? "sort-asc" : "sort-desc");
    applySortToFiltered();
    renderTable();
  });
});

searchInput.addEventListener("input", applyFilter);

/* ── Charts ── */
function updateCharts(stats) {
  buildBar("deptChart",   stats.departments, "Employees");
  buildPie("roleChart",   stats.roles);
  buildBar("genderChart", stats.genders, "Employees");
}

function buildBar(id, dataObj, label) {
  const labels = Object.keys(dataObj);
  const values = Object.values(dataObj);
  if (chartInstances[id]) chartInstances[id].destroy();
  chartInstances[id] = new Chart(document.getElementById(id), {
    type: "bar",
    data: {
      labels,
      datasets: [{ label, data: values, backgroundColor: CHART_COLORS.slice(0, labels.length), borderRadius: 5 }],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: "#7A90B0", maxRotation: 35 }, grid: { color: "#2E3D56" } },
        y: { ticks: { color: "#7A90B0", stepSize: 1 }, grid: { color: "#2E3D56" }, beginAtZero: true },
      },
    },
  });
}

function buildPie(id, dataObj) {
  const labels = Object.keys(dataObj);
  const values = Object.values(dataObj);
  if (chartInstances[id]) chartInstances[id].destroy();
  chartInstances[id] = new Chart(document.getElementById(id), {
    type: "pie",
    data: {
      labels,
      datasets: [{ data: values, backgroundColor: CHART_COLORS.slice(0, labels.length) }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "bottom", labels: { color: "#DCE8FA", padding: 14 } },
      },
    },
  });
}

/* ── Modal: Add ── */
document.getElementById("openAddModal").addEventListener("click", openAdd);
document.getElementById("modalClose").addEventListener("click", closeModal);
document.getElementById("cancelBtn").addEventListener("click", closeModal);
modalOverlay.addEventListener("click", e => { if (e.target === modalOverlay) closeModal(); });

function openAdd() {
  editingId = null;
  empForm.reset();
  clearErrors();
  idField.disabled = false;
  modalTitle.textContent = "Add Employee";
  submitBtn.textContent  = "Add Employee";
  modalOverlay.hidden = false;
  idField.focus();
}

function openEdit(id) {
  const emp = employees.find(e => e.id === id);
  if (!emp) return;
  editingId = id;
  empForm.reset();
  clearErrors();
  idField.value = emp.id;
  idField.disabled = true;
  document.getElementById("f-name").value   = emp.name;
  document.getElementById("f-dept").value   = emp.department;
  document.getElementById("f-role").value   = emp.role;
  document.getElementById("f-gender").value = emp.gender;
  modalTitle.textContent = "Edit Employee";
  submitBtn.textContent  = "Save Changes";
  modalOverlay.hidden = false;
  document.getElementById("f-name").focus();
}

function closeModal() {
  modalOverlay.hidden = true;
  empForm.reset();
  clearErrors();
  idField.disabled = false;
  editingId = null;
}

/* ── Modal: Delete ── */
document.getElementById("deleteModalClose").addEventListener("click", closeDelete);
document.getElementById("cancelDeleteBtn").addEventListener("click", closeDelete);
deleteOverlay.addEventListener("click", e => { if (e.target === deleteOverlay) closeDelete(); });
document.getElementById("confirmDeleteBtn").addEventListener("click", async () => {
  if (!deleteTargetId) return;
  try {
    await api("DELETE", `/api/employees/${encodeURIComponent(deleteTargetId)}`);
    showToast("Employee deleted successfully");
    closeDelete();
    await refresh();
  } catch (e) {
    showToast(e.message, "error");
  }
});

function openDelete(id, name) {
  deleteTargetId = id;
  document.getElementById("deleteEmpName").textContent = name;
  deleteOverlay.hidden = false;
}

function closeDelete() {
  deleteOverlay.hidden = true;
  deleteTargetId = null;
}

/* ── Form submission ── */
empForm.addEventListener("submit", async e => {
  e.preventDefault();
  clearErrors();

  const id         = idField.value.trim();
  const name       = document.getElementById("f-name").value.trim();
  const department = document.getElementById("f-dept").value;
  const role       = document.getElementById("f-role").value;
  const gender     = document.getElementById("f-gender").value;

  let valid = true;
  if (!editingId && !id)   { setError("err-id",     "ID is required");         valid = false; }
  if (!name)                { setError("err-name",   "Name is required");       valid = false; }
  else if (!/^[A-Za-z\s]+$/.test(name)) { setError("err-name", "Alphabets only"); valid = false; }
  if (!department)          { setError("err-dept",   "Select a department");    valid = false; }
  if (!role)                { setError("err-role",   "Select a role");          valid = false; }
  if (!gender)              { setError("err-gender", "Select a gender");        valid = false; }
  if (!valid) return;

  const body = { id, name, department, role, gender };
  try {
    if (editingId) {
      await api("PUT", `/api/employees/${encodeURIComponent(editingId)}`, body);
      showToast("Employee updated successfully");
    } else {
      await api("POST", "/api/employees", body);
      showToast("Employee added successfully");
    }
    closeModal();
    await refresh();
  } catch (err) {
    showToast(err.message, "error");
  }
});

function setError(id, msg) {
  document.getElementById(id).textContent = msg;
}
function clearErrors() {
  ["err-id","err-name","err-dept","err-role","err-gender"].forEach(id => {
    document.getElementById(id).textContent = "";
  });
}

/* ── Keyboard: Escape closes modals ── */
document.addEventListener("keydown", e => {
  if (e.key === "Escape") {
    if (!modalOverlay.hidden)  closeModal();
    if (!deleteOverlay.hidden) closeDelete();
  }
});

/* ── Start ── */
init();
