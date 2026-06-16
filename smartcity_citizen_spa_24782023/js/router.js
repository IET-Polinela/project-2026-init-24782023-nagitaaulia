const routes = {
  login: `
    <section class="row justify-content-center mt-5">
      <div class="col-12 col-md-6 col-lg-4 card shadow-sm border-0 p-4">

        <h3 class="text-center fw-bold mb-4">
          <i class="bi bi-person-circle me-2"></i>
          Login Warga
        </h3>

        <form id="login-form">

          <div class="mb-3">
            <label class="form-label">
              Username
            </label>

            <input
              type="text"
              id="loginUsername"
              class="form-control"
              required>
          </div>

          <div class="mb-3">
            <label class="form-label">
              Password
            </label>

            <input
              type="password"
              id="loginPassword"
              class="form-control"
              required>
          </div>

          <button
            type="submit"
            class="btn btn-primary w-100 fw-bold">
            Login
          </button>

        </form>

      </div>
    </section>
  `,

  dashboard: `
    <section class="row g-4">

      <aside class="col-lg-3">

        <div class="card p-3 shadow-sm">

          <h5>Rekap Status</h5>

          <div class="mt-3">
            <strong>Draft :</strong>
            <span id="draftCount">0</span>
          </div>

          <div>
            <strong>Diproses :</strong>
            <span id="processCount">0</span>
          </div>

          <div>
            <strong>Selesai :</strong>
            <span id="doneCount">0</span>
          </div>

          <button
            class="btn btn-primary w-100 mt-3"
            onclick="openCreateModal()">

            Tambah Laporan Baru

          </button>

        </div>

      </aside>

      <section class="col-lg-9">

        <div class="card p-3 shadow-sm">

          <ul class="nav nav-tabs mb-3">

            <li class="nav-item">
              <button
                class="nav-link active"
                onclick="loadDashboardData('my_reports',1)">
                Laporan Saya
              </button>
            </li>

            <li class="nav-item">
              <button
                class="nav-link"
                onclick="loadDashboardData('feed',1)">
                Feed Kota
              </button>
            </li>

          </ul>

          <div id="listContainer"></div>

          <div
            id="paginationContainer"
            class="mt-3">
          </div>

        </div>

      </section>

    </section>

    <!-- MODAL REPORT -->

    <div
      class="modal fade"
      id="reportModal"
      tabindex="-1">

      <div class="modal-dialog">

        <div class="modal-content">

          <div class="modal-header">

            <h5 class="modal-title">
              Form Laporan
            </h5>

            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal">
            </button>

          </div>

          <div class="modal-body">

            <form id="reportForm">

              <input
                type="text"
                id="title"
                class="form-control mb-2"
                placeholder="Judul Laporan"
                required>

              <input
                type="text"
                id="category"
                class="form-control mb-2"
                placeholder="Kategori"
                required>

              <input
                type="text"
                id="location"
                class="form-control mb-2"
                placeholder="Lokasi"
                required>

              <textarea
                id="description"
                class="form-control"
                rows="4"
                placeholder="Deskripsi Laporan"
                required>
              </textarea>

            </form>

          </div>

          <div class="modal-footer">

            <button
              type="button"
              class="btn btn-warning"
              onclick="submitReport('DRAFT')">

              Simpan Draft

            </button>

            <button
              type="button"
              class="btn btn-primary"
              onclick="submitReport('REPORTED')">

              Ajukan

            </button>

          </div>

        </div>

      </div>

    </div>
  `
};

function handleRouting() {

  const app =
  document.getElementById(
    "app-content"
  );

  const hash =
  window.location.hash
  .replace("#","")
  || "login";

  app.innerHTML =
  routes[hash]
  || routes.login;

  updateNavbar();

  if(hash === "login")
  {
      setupLoginForm();
  }

  if(hash === "dashboard")
  {
      const token =
      localStorage.getItem(
          "access_token"
      );

      if(!token)
      {
          window.location.hash =
          "#login";
          return;
      }

      loadDashboardData(
          "my_reports",
          1
      );
  }
}

window.addEventListener(
  "hashchange",
  handleRouting
);

window.addEventListener(
  "DOMContentLoaded",
  handleRouting
);