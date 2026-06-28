from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Jalur untuk halaman utama dashboard
    path('', views.DashboardView.as_view(), name='index'),
    
    # Jalur untuk mengambil data JSON (Fetch API)
    path('api/stats/', views.dashboard_data, name='stats'),
]