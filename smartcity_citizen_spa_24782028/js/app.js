const PAGE_SIZE = 10;

let currentTab = 'feed';
let currentPage = 1;
let allReports = [];
let editingReportId = null;

function updateNavbar() {
    const navMenus = document.getElementById('nav-menus');
    if (!navMenus) return;

    const token = localStorage.getItem('access_token');

    if (token) {
        navMenus.innerHTML = `
            <button id="logoutBtn" class="btn btn-outline-light btn-sm fw-bold">
                <i class="bi bi-box-arrow-right me-1"></i>Keluar
            </button>
        `;
        
        document.getElementById('logoutBtn').addEventListener('click', function() {
            localStorage.clear();
            alert('Anda telah keluar.');
            window.location.hash = '#login';
            updateNavbar();
        });
    } else {
        navMenus.innerHTML = '';
    }
}

function getToken() {
    return localStorage.getItem('access_token');
}

async function requestWithAuth(endpoint, options = {}) {
    const token = getToken();

    if (!token) {
        throw new Error('Token tidak ditemukan. Silakan login kembali.');
    }

    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...(options.headers || {})
    };

    const response = await fetch(`${BASE_URL}${endpoint}`, {
        ...options,
        headers
    });

    if (!response.ok) {
        let message = 'Gagal memuat data dari server.';

        try {
            const errorData = await response.json();
            message = errorData.detail || JSON.stringify(errorData);
        } catch (error) {
            message = response.statusText || message;
        }

        throw new Error(message);
    }

    return response;
}

async function fetchWithAuth(endpoint, options = {}) {
    const response = await requestWithAuth(endpoint, options);

    if (response.status === 204) {
        return null;
    }

    return response.json();
}

function escapeHTML(value) {
    return String(value ?? '').replace(/[&<>"']/g, (char) => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    }[char]));
}

function getStatusConfig(status) {
    const configs = {
        DRAFT: { percent: 25, color: 'warning', label: 'Draft' },
        REPORTED: { percent: 50, color: 'info', label: 'Dilaporkan' },
        VERIFIED: { percent: 60, color: 'info', label: 'Diverifikasi' },
        IN_PROGRESS: { percent: 75, color: 'primary', label: 'Diproses' },
        DONE: { percent: 100, color: 'success', label: 'Selesai' },
        RESOLVED: { percent: 100, color: 'success', label: 'Selesai' }
    };

    return configs[status] || { percent: 0, color: 'secondary', label: status || 'Tidak diketahui' };
}

function setDashboardLoading() {
    const reportList = document.getElementById('reportList');
    const paginationContainer = document.getElementById('paginationContainer');

    if (reportList) {
        reportList.innerHTML = `
            <div class="card border-0 shadow-sm">
                <div class="card-body text-center text-muted py-5">
                    <div class="spinner-border text-primary mb-3" role="status"></div>
                    <p class="mb-0">Memuat laporan...</p>
                </div>
            </div>
        `;
    }

    if (paginationContainer) {
        paginationContainer.innerHTML = '';
    }
}

function showDashboardError(message) {
    const reportError = document.getElementById('reportError');
    const reportList = document.getElementById('reportList');
    const paginationContainer = document.getElementById('paginationContainer');

    if (reportError) {
        reportError.textContent = message;
        reportError.classList.remove('d-none');
    }

    if (reportList) {
        reportList.innerHTML = `
            <div class="card border-0 shadow-sm">
                <div class="card-body text-center text-muted py-5">
                    <i class="bi bi-exclamation-triangle fs-1 text-danger"></i>
                    <h5 class="mt-3">Data belum bisa dimuat</h5>
                    <p class="small mb-0">${escapeHTML(message)}</p>
                </div>
            </div>
        `;
    }

    if (paginationContainer) {
        paginationContainer.innerHTML = '';
    }
}

function setActiveTab(tab) {
    const dashboardTitle = document.getElementById('dashboardTitle');

    document.querySelectorAll('#dashboardTabs [data-tab]').forEach((button) => {
        button.classList.toggle('active', button.dataset.tab === tab);
    });

    if (dashboardTitle) {
        dashboardTitle.textContent = tab === 'my_reports' ? 'Laporan Saya' : 'Feed Laporan';
    }
}

async function loadDashboardData(tab = currentTab, page = 1) {
    currentTab = tab;
    currentPage = page;
    setActiveTab(tab);
    setDashboardLoading();
    loadSummaryStats(tab);

    const reportError = document.getElementById('reportError');
    if (reportError) {
        reportError.classList.add('d-none');
        reportError.textContent = '';
    }

    try {
        const data = await fetchWithAuth(`/api/report/?tab=${encodeURIComponent(tab)}&page=${page}`);
        allReports = data.results || [];
        const totalPages = Math.ceil((data.count || 0) / PAGE_SIZE);

        renderList(allReports);
        renderPagination(totalPages);
    } catch (error) {
        showDashboardError(error.message);
    }
}

function renderList(reports) {
    const reportList = document.getElementById('reportList');
    if (!reportList) return;

    if (!reports.length) {
        reportList.innerHTML = `
            <div class="card border-0 shadow-sm">
                <div class="card-body text-center text-muted py-5">
                    <i class="bi bi-inbox fs-1"></i>
                    <h5 class="mt-3">Belum ada laporan</h5>
                    <p class="small mb-0">Data laporan untuk tab ini masih kosong.</p>
                </div>
            </div>
        `;
        return;
    }

    reportList.innerHTML = reports.map((report) => {
        const status = getStatusConfig(report.status);
        const createdAt = report.created_at
            ? new Date(report.created_at).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
            : '-';
        const editButton = report.is_owner === true && report.status === 'DRAFT'
            ? `<button type="button" class="btn btn-sm btn-outline-primary" onclick="editDraft(${report.id})">
                    <i class="bi bi-pencil-square me-1"></i>Edit
               </button>`
            : '';

        return `
            <article class="card border-0 shadow-sm">
                <div class="card-body">
                    <div class="d-flex justify-content-between gap-3 align-items-start mb-2">
                        <div>
                            <h5 class="fw-bold mb-1">${escapeHTML(report.title)}</h5>
                            <div class="small text-muted">
                                <i class="bi bi-person-circle me-1"></i>${escapeHTML(report.reporter || 'Warga Anonim')}
                                <span class="mx-2">|</span>
                                <i class="bi bi-tag me-1"></i>${escapeHTML(report.category)}
                                <span class="mx-2">|</span>
                                <i class="bi bi-geo-alt me-1"></i>${escapeHTML(report.location)}
                            </div>
                        </div>
                        <span class="badge bg-${status.color} ${status.color === 'warning' ? 'text-dark' : ''}">
                            ${escapeHTML(status.label)}
                        </span>
                    </div>
                    <p class="text-secondary mb-3">${escapeHTML(report.description)}</p>
                    <div class="progress mb-3" style="height: 8px;" role="progressbar" aria-valuenow="${status.percent}" aria-valuemin="0" aria-valuemax="100">
                        <div class="progress-bar bg-${status.color}" style="width: ${status.percent}%"></div>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="small text-muted">
                            <i class="bi bi-clock-history me-1"></i>${createdAt}
                        </span>
                        ${editButton}
                    </div>
                </div>
            </article>
        `;
    }).join('');
}

function renderPagination(totalPages) {
    const paginationContainer = document.getElementById('paginationContainer');
    if (!paginationContainer) return;

    if (totalPages <= 1) {
        paginationContainer.innerHTML = '';
        return;
    }

    paginationContainer.innerHTML = Array.from({ length: totalPages }, (_, index) => {
        const pageNumber = index + 1;
        const isActive = pageNumber === currentPage;

        return `
            <li class="page-item ${isActive ? 'active' : ''}">
                <button type="button" class="page-link ${isActive ? 'active' : ''}" onclick="loadDashboardData('${currentTab}', ${pageNumber})">
                    ${pageNumber}
                </button>
            </li>
        `;
    }).join('');
}

function updateSummaryElement(id, value) {
    const element = document.getElementById(id);
    if (element) element.textContent = value;
}

async function loadSummaryStats(tab = currentTab) {
    try {
        const data = await fetchWithAuth(`/api/report/?tab=${encodeURIComponent(tab)}&page_size=1000`);
        const reports = data.results || [];
        const totalDraft = reports.filter((report) => report.status === 'DRAFT').length;
        const totalReported = reports.filter((report) => report.status === 'REPORTED').length;
        const totalVerified = reports.filter((report) => report.status === 'VERIFIED').length;
        const totalInProgress = reports.filter((report) => report.status === 'IN_PROGRESS').length;
        const totalResolved = reports.filter((report) => ['DONE', 'RESOLVED'].includes(report.status)).length;

        updateSummaryElement('summaryDraft', totalDraft);
        updateSummaryElement('summaryReported', totalReported);
        updateSummaryElement('summaryVerified', totalVerified);
        updateSummaryElement('summaryInProgress', totalInProgress);
        updateSummaryElement('summaryResolved', totalResolved);
    } catch (error) {
        console.error('Gagal memuat ringkasan laporan:', error);
        updateSummaryElement('summaryDraft', 0);
        updateSummaryElement('summaryReported', 0);
        updateSummaryElement('summaryVerified', 0);
        updateSummaryElement('summaryInProgress', 0);
        updateSummaryElement('summaryResolved', 0);
    }
}

function resetReportModal() {
    const reportForm = document.getElementById('reportForm');
    const reportFormError = document.getElementById('reportFormError');
    const reportModalTitle = document.getElementById('reportModalTitle');

    editingReportId = null;

    if (reportForm) {
        reportForm.reset();
        reportForm.classList.remove('was-validated');
    }

    if (reportFormError) {
        reportFormError.classList.add('d-none');
        reportFormError.textContent = '';
    }

    if (reportModalTitle) {
        reportModalTitle.textContent = 'Laporan Baru';
    }
}

function openReportModal() {
    resetReportModal();
    const reportModal = document.getElementById('reportModal');
    bootstrap.Modal.getOrCreateInstance(reportModal).show();
}

async function editDraft(id) {
    try {
        const report = await fetchWithAuth(`/api/report/${id}/`);

        document.getElementById('reportTitle').value = report.title || '';
        document.getElementById('reportCategory').value = report.category || '';
        document.getElementById('reportLocation').value = report.location || '';
        document.getElementById('reportDescription').value = report.description || '';
        document.getElementById('reportModalTitle').textContent = 'Edit Draft';

        editingReportId = id;

        const reportModal = document.getElementById('reportModal');
        bootstrap.Modal.getOrCreateInstance(reportModal).show();
    } catch (error) {
        showDashboardError(error.message);
    }
}

function getReportPayload(status) {
    return {
        title: document.getElementById('reportTitle').value.trim(),
        category: document.getElementById('reportCategory').value,
        location: document.getElementById('reportLocation').value.trim(),
        description: document.getElementById('reportDescription').value.trim(),
        status
    };
}

function setModalSubmitting(isSubmitting) {
    const btnDraft = document.getElementById('btnDraft');
    const btnSubmit = document.getElementById('btnSubmit');

    if (btnDraft) btnDraft.disabled = isSubmitting;
    if (btnSubmit) btnSubmit.disabled = isSubmitting;
}

async function submitReport(status) {
    const reportForm = document.getElementById('reportForm');
    const reportFormError = document.getElementById('reportFormError');

    if (!reportForm.checkValidity()) {
        reportForm.classList.add('was-validated');
        return;
    }

    if (reportFormError) {
        reportFormError.classList.add('d-none');
        reportFormError.textContent = '';
    }

    const endpoint = editingReportId === null ? '/api/report/' : `/api/report/${editingReportId}/`;
    const method = editingReportId === null ? 'POST' : 'PUT';
    const payload = getReportPayload(status);

    try {
        setModalSubmitting(true);
        const response = await requestWithAuth(endpoint, {
            method,
            body: JSON.stringify(payload)
        });

        if (![200, 201].includes(response.status)) {
            throw new Error('Laporan tersimpan, tetapi server mengembalikan status yang tidak dikenali.');
        }

        const reportModal = document.getElementById('reportModal');
        bootstrap.Modal.getOrCreateInstance(reportModal).hide();
        reportForm.reset();
        reportForm.classList.remove('was-validated');
        editingReportId = null;

        await loadDashboardData(currentTab, currentPage);
        await loadSummaryStats(currentTab);
    } catch (error) {
        if (reportFormError) {
            reportFormError.textContent = error.message;
            reportFormError.classList.remove('d-none');
        }
    } finally {
        setModalSubmitting(false);
    }
}

function setupReportModal() {
    const btnDraft = document.getElementById('btnDraft');
    const btnSubmit = document.getElementById('btnSubmit');

    if (btnDraft) {
        btnDraft.addEventListener('click', () => submitReport('DRAFT'));
    }

    if (btnSubmit) {
        btnSubmit.addEventListener('click', () => submitReport('REPORTED'));
    }
}

function setupDashboard() {
    const btnOpenReportModal = document.getElementById('btnOpenReportModal');

    if (btnOpenReportModal) {
        btnOpenReportModal.addEventListener('click', openReportModal);
    }

    document.querySelectorAll('#dashboardTabs [data-tab]').forEach((button) => {
        button.addEventListener('click', () => loadDashboardData(button.dataset.tab, 1));
    });

    loadDashboardData(currentTab, currentPage);
}

document.addEventListener('DOMContentLoaded', () => {
    updateNavbar();
    setupReportModal();
});
