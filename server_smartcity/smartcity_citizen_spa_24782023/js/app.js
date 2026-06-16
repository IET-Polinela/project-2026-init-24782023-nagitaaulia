function updateNavbar() {
  const navMenu = document.getElementById("nav-menu");
  const token = localStorage.getItem("access_token");

  if (token) {
    navMenu.innerHTML = `
      <button class="btn btn-light btn-sm" onclick="logout()">
        <i class="bi bi-box-arrow-right me-1"></i>Logout
      </button>
    `;
  } else {
    navMenu.innerHTML = `
      <a href="#login" class="btn btn-light btn-sm">
        <i class="bi bi-box-arrow-in-right me-1"></i>Login
      </a>
    `;
  }
}

// ======================
// LAB SESSION 12
// ======================

let currentTab = "my_reports";
let currentPage = 1;
let editingReportId = null;

// ======================
// MODAL CREATE
// ======================

function openCreateModal() {

  const username =
    localStorage.getItem(
      "username"
    );

  if (
    username &&
    username.toLowerCase() === "admin"
  ) {
    alert(
      "Admin tidak diperbolehkan membuat laporan."
    );
    return;
  }

  editingReportId = null;

  const form =
    document.getElementById(
      "reportForm"
    );

  if(form){
    form.reset();
  }

  const modal =
    new bootstrap.Modal(
      document.getElementById(
        "reportModal"
      )
    );

  modal.show();
}

// ======================
// LOAD DASHBOARD
// ======================

async function loadDashboardData(
  tab = currentTab,
  page = currentPage
) {

  currentTab = tab;
  currentPage = page;

  const response = await requestAPI(
    `/report/?tab=${tab}&page=${page}`
  );

  if (!response.ok) {
    console.error(response);
    return;
  }

  const reports =
    response.data.results || [];

  renderList(reports);

  renderPagination(
    response.data.count || 0
  );

  await loadSummaryStats();
}

// ======================
// RENDER LIST
// ======================

function renderList(reports) {

  const container =
    document.getElementById(
      "listContainer"
    );

  if (!container) return;

  container.innerHTML = "";

  if (reports.length === 0) {

    container.innerHTML = `
      <div class="alert alert-info">
        Belum ada laporan.
      </div>
    `;

    return;
  }

  reports.forEach(report => {

    let progress = 0;

    switch (report.status) {

      case "DRAFT":
        progress = 20;
        break;

      case "REPORTED":
        progress = 40;
        break;

      case "VERIFIED":
        progress = 60;
        break;

      case "IN_PROGRESS":
        progress = 80;
        break;

      case "RESOLVED":
        progress = 100;
        break;
    }

    container.innerHTML += `

      <div class="card shadow-sm mb-3">

        <div class="card-body">

          <h5>
            ${report.title}
          </h5>

          <small class="text-muted d-block mb-2">
            Pelapor: ${report.reporter}
          </small>

          <p>
            ${report.description}
          </p>

          <div class="mb-2">

            <span class="badge bg-secondary">
              ${report.category}
            </span>

            <span class="badge bg-info">
              ${report.location}
            </span>

          </div>

          <div class="progress mt-3">

            <div
              class="progress-bar"
              role="progressbar"
              style="width:${progress}%">

              ${report.status}

            </div>

          </div>

          ${
            report.status === "DRAFT"
            && report.is_owner

              ?

            `
              <button
                class="btn btn-warning btn-sm mt-3"
                onclick="editDraft(${report.id})">

                Edit Draft

              </button>
            `

              :

            ""
          }

        </div>

      </div>

    `;
  });
}

// ======================
// PAGINATION
// ======================

function renderPagination(totalItems) {

  const container =
    document.getElementById(
      "paginationContainer"
    );

  if (!container) return;

  container.innerHTML = "";

  const totalPages =
    Math.ceil(totalItems / 10);

  for (
    let i = 1;
    i <= totalPages;
    i++
  ) {

    container.innerHTML += `

      <button
        class="btn btn-outline-primary btn-sm me-1"
        onclick="loadDashboardData(
          '${currentTab}',
          ${i}
        )">

        ${i}

      </button>

    `;
  }
}

// ======================
// SIDEBAR SUMMARY
// ======================

async function loadSummaryStats() {

  const response =
    await requestAPI(
      "/report/?tab=my_reports&page_size=1000"
    );

  if (!response.ok) {
    return;
  }

  const reports =
    response.data.results || [];

  document.getElementById(
    "draftCount"
  ).innerText =
    reports.filter(
      r => r.status === "DRAFT"
    ).length;

  document.getElementById(
    "processCount"
  ).innerText =
    reports.filter(
      r =>
        r.status === "VERIFIED" ||
        r.status === "IN_PROGRESS"
    ).length;

  document.getElementById(
    "doneCount"
  ).innerText =
    reports.filter(
      r => r.status === "RESOLVED"
    ).length;

}

// ======================
// EDIT DRAFT
// ======================

async function editDraft(id) {

  const response =
    await requestAPI(
      `/report/${id}/`
    );

  if (!response.ok) {
    return;
  }

  const report =
    response.data;

  editingReportId = id;

  document.getElementById(
    "title"
  ).value = report.title;

  document.getElementById(
    "category"
  ).value = report.category;

  document.getElementById(
    "location"
  ).value = report.location;

  document.getElementById(
    "description"
  ).value = report.description;

  const modal =
    new bootstrap.Modal(
      document.getElementById(
        "reportModal"
      )
    );

  modal.show();
}


// ======================
// SUBMIT REPORT
// ======================

async function submitReport(status) {

  const payload = {
    title: document.getElementById("title").value,
    category: document.getElementById("category").value,
    location: document.getElementById("location").value,
    description: document.getElementById("description").value,
    status: status
  };

  let response;

  try {

    if (editingReportId === null) {

      response = await requestAPI(
        "/report/",
        "POST",
        payload
      );

    } else {

      response = await requestAPI(
        `/report/${editingReportId}/`,
        "PUT",
        payload
      );

    }

    if (
      response.status === 200 ||
      response.status === 201
    ) {

      alert("Laporan berhasil disimpan!");

      document
        .getElementById("reportForm")
        .reset();

      editingReportId = null;

      const modal =
        bootstrap.Modal.getInstance(
          document.getElementById("reportModal")
        );

      if (modal) {
        modal.hide();
      }

      loadDashboardData(
        currentTab,
        currentPage
      );

    } else {

      alert(
        JSON.stringify(response.data)
      );

    }

  } catch (error) {

    console.error(
      "Submit Error:",
      error
    );

    alert(
      "Terjadi kesalahan saat menyimpan laporan!"
    );

  }

}