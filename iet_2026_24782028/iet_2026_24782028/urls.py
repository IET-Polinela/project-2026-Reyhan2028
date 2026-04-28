from django.contrib import admin
from django.urls import path, include
from usermanagement_2028 import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', user_views.register, name='register'),
    
    # 1. Jalur untuk Main App (Halaman Utama)
    path('', include('main_app.urls')), 
    
    # 2. Jalur untuk App About
    path('about/', include('about.urls')), 
    
    # 3. Jalur untuk App Contacts
    path('contacts/', include('contacts.urls')), 

    # --- UPDATE UNTUK LAB 6 (Authentication dengan Feedback) ---
    
    # Login: Menggunakan UserLoginView kustom agar pesan sukses muncul
    path('login/', user_views.UserLoginView.as_view(), name='login'),
    
    # Logout: Menggunakan UserLogoutView kustom agar pesan logout muncul
    path('logout/', user_views.UserLogoutView.as_view(next_page='login'), name='logout'),
]