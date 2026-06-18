const routes = {
    '#login': `
        <div class="row justify-content-center mt-5">
            <div class="col-md-4 card shadow-sm border-0 p-4">
                <h4 class="text-center fw-bold mb-4">Login Warga</h4>
                <form id="loginForm">
                    <div class="mb-3">
                        <input type="text" id="loginUsername" class="form-control mb-3" placeholder="Username" required>
                        <input type="password" id="loginPassword" class="form-control mb-3" placeholder="Password" required>
                        <button type="submit" class="btn btn-primary w-100 fw-bold">Masuk</button>
                    </div>
                </form>
            </div>
        </div>
    `,
    '#dashboard': `
        <div class="row g-4">
            <aside class="col-12 col-lg-3">
                <div class="card border-0 p-3 shadow-sm sticky-top" style="top: 20px;">
                    <button type="button" id="btnOpenReportModal" class="btn btn-primary btn-lg w-100 fw-bold mb-3">
                        <i class="bi bi-plus-circle-fill me-2"></i>Laporan Baru
                    </button>
                    <div class="list-group mb-4" id="dashboardTabs">
                        <button type="button" class="list-group-item list-group-item-action active" data-tab="feed">
                            <i class="bi bi-broadcast-pin me-2"></i>Feed Laporan
                        </button>
                        <button type="button" class="list-group-item list-group-item-action" data-tab="my_reports">
                            <i class="bi bi-person-lines-fill me-2"></i>Laporan Saya
                        </button>
                    </div>
                    <h6 class="fw-bold text-uppercase small text-muted mb-3">Ringkasan Status</h6>
                    <div class="d-grid gap-2">
                        <div class="d-flex justify-content-between align-items-center bg-light rounded p-2">
                            <span class="small">Draft</span>
                            <span id="summaryDraft" class="badge bg-warning text-dark">0</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center bg-light rounded p-2">
                            <span class="small">Reported</span>
                            <span id="summaryReported" class="badge bg-info">0</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center bg-light rounded p-2">
                            <span class="small">Verified</span>
                            <span id="summaryVerified" class="badge bg-info">0</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center bg-light rounded p-2">
                            <span class="small">In Progress</span>
                            <span id="summaryInProgress" class="badge bg-primary">0</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center bg-light rounded p-2">
                            <span class="small">Resolved</span>
                            <span id="summaryResolved" class="badge bg-success">0</span>
                        </div>
                    </div>
                </div>
            </aside>
            <section class="col-12 col-lg-6">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h4 class="fw-bold mb-0" id="dashboardTitle">Feed Laporan</h4>
                </div>
                <div id="reportError" class="alert alert-danger d-none" role="alert"></div>
                <div id="reportList" class="d-grid gap-3"></div>
                <nav aria-label="Navigasi halaman laporan" class="mt-4">
                    <ul id="paginationContainer" class="pagination justify-content-center"></ul>
                </nav>
            </section>
            <aside class="col-lg-3 d-none d-lg-block">
                <div class="card border-0 p-3 shadow-sm sticky-top" style="top: 20px;">
                    <h6 class="fw-bold"><i class="bi bi-info-circle-fill text-primary me-2"></i>Pengumuman</h6>
                    <p class="small text-muted mb-0">Pantau laporan warga terbaru dan kelola draft Anda tanpa reload halaman.</p>
                </div>
            </aside>
        </div>
    `
};

function handleRouting() {
    const hash = window.location.hash || '#login'; // Default ke login

    if (hash === '#dashboard' && !localStorage.getItem('access_token')) {
        window.location.hash = '#login';
        return;
    }

    document.getElementById('app-content').innerHTML = routes[hash] || routes['#login'];
    if (hash === '#login' && typeof setupLoginForm === 'function') setupLoginForm();
    if (hash === '#dashboard' && typeof setupDashboard === 'function') setupDashboard();
}

window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);
