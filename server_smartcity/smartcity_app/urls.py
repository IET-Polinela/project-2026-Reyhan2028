from django.contrib import admin
from django.urls import path, include
from usermanagement_2028 import views as user_views

# --- TAMBAHAN BARU UNTUK LAB 10 (Hanya menambah impor ini) ---
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# --- UPDATE LAB 10: TAMBAHKAN IMPOR INI (Untuk Register API) ---
from usermanagement_2028.api_views import RegisterView

# --- TAMBAHAN BARU UNTUK LAB 14 (OpenAPI Documentation) ---
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django_scalar.views import scalar_viewer

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- TAMBAHAN BARU UNTUK LAB 14 (OpenAPI Documentation) ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(
        'api/docs/scalar/',
        scalar_viewer,
        {'openapi_url': '/api/schema/', 'title': 'Smart City Portal API'},
        name='scalar',
    ),

    path('register/', user_views.register, name='register'),
    
    # --- UPDATE UNTUK LAB 9 (REST API) ---
    # Path dasar api/ untuk mengakses endpoint reports
    path('api/', include('main_app.api_urls')), 
    
    # --- TAMBAHAN BARU LAB 10 (Agar Tombol Login & Form POST Muncul di Browser) ---
    path('api-auth/', include('rest_framework.urls')),
    
    # --- TAMBAHAN BARU UNTUK LAB 10 ---
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # --- UPDATE LAB 10: TAMBAHKAN BARIS INI (Endpoint Register API Baru) ---
    path('api/register/', RegisterView.as_view(), name='api_register'),
    
    # 1. Jalur untuk Main App (Halaman Utama)
    path('', include('main_app.urls')), 
    
    # 2. Jalur untuk App About
    path('about/', include('about.urls')), 
    
    # 3. Jalur untuk App Contacts
    path('contacts/', include('contacts.urls')), 

    # 4. JALUR UNTUK APP DASHBOARD (Update Lab 7)
    path('dashboard/', include('dashboard_2028.urls')),

    # --- UPDATE UNTUK LAB 6 (Authentication dengan Feedback) ---
    path('login/', user_views.UserLoginView.as_view(), name='login'),
    
    path('logout/', user_views.UserLogoutView.as_view(next_page='login'), name='logout'),
]
