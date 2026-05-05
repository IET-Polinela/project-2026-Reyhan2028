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

    # 4. JALUR UNTUK APP DASHBOARD (Update Lab 7)
    path('dashboard/', include('dashboard_2028.urls')), # <--- Tambahkan ini!

    # --- UPDATE UNTUK LAB 6 (Authentication dengan Feedback) ---
    
    path('login/', user_views.UserLoginView.as_view(), name='login'),
    
    path('logout/', user_views.UserLogoutView.as_view(next_page='login'), name='logout'),
]