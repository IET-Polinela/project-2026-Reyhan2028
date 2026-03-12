from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Jalur untuk Main App (Halaman Utama)
    path('', include('main_app.urls')), 
    
    # 2. Jalur untuk App About (Akses lewat /about/)
    path('about/', include('about.urls')), 
    
    # 3. Jalur untuk App Contacts (Akses lewat /contacts/)
    path('contacts/', include('contacts.urls')), 
]