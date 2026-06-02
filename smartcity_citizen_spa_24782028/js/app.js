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

document.addEventListener('DOMContentLoaded', () => {
    updateNavbar();
});