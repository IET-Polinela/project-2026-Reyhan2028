/**
 * Fungsi untuk mengontrol formulir login warga
 */
function setupLoginForm() {
    const form = document.getElementById('loginForm');
    if (!form) return;

    form.addEventListener('submit', async function(e) {
        // Wajib gunakan preventDefault agar halaman tidak reload saat disubmit
        e.preventDefault(); 
        
        const usernameInput = document.getElementById('loginUsername').value;
        const passwordInput = document.getElementById('loginPassword').value;

        const payload = {
            username: usernameInput,
            password: passwordInput
        };

        // Menembak endpoint token menggunakan fungsi requestAPI dari api.js
        try {
            const data = await requestAPI('/api/token/', 'POST', payload);

            // Simpan access dan refresh token ke dalam localStorage browser jika sukses
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            
            alert('Login Berhasil!');
            
            // Mengubah rute halaman secara instan ke dashboard via hash URL
            window.location.hash = '#dashboard';
            
            // Perbarui tampilan navbar (menampilkan tombol logout)
            if (typeof updateNavbar === 'function') {
                updateNavbar();
            }
        } catch (error) {
            alert('Login Gagal: Username atau password salah!');
            console.error(error);
        }
    });
}
