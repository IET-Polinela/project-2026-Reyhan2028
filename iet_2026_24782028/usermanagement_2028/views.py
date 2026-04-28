from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CitizenRegistrationForm

# 1. Registrasi Citizen (Sudah ditambahkan pesan sukses)
def register(request):
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Feedback: Berhasil Registrasi
            messages.success(request, 'Akun Citizen berhasil dibuat! Silakan gunakan akun tersebut untuk login.')
            return redirect('login')
    else:
        form = CitizenRegistrationForm()
    return render(request, 'usermanagement_2028/register.html', {'form': form})

# 2. Login View (Menambahkan pesan selamat datang)
class UserLoginView(LoginView):
    template_name = 'usermanagement_2028/login.html'
    
    def form_valid(self, form):
        # Feedback: Berhasil Login
        messages.success(self.request, f"Selamat datang, {form.get_user().username}!")
        return super().form_valid(form)

# 3. Logout View (Menambahkan pesan setelah keluar)
class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Feedback: Berhasil Logout
        if request.method == 'POST':
            messages.info(request, "Anda telah berhasil keluar dari aplikasi.")
        return super().dispatch(request, *args, **kwargs)