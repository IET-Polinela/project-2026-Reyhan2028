from django.urls import path
from . import views

urlpatterns = [
    # 1. Halaman Penyambutan (Home)
    path('', views.IndexView.as_view(), name='index'), 
    
    # 2. Halaman Daftar Laporan (Reports)
    path('reports/', views.ReportListView.as_view(), name='home'), 
    
    # 3. Fitur CRUD & Workflow
    path('add/', views.ReportCreateView.as_view(), name='add_report'),
    path('detail/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('update/<int:pk>/', views.ReportUpdateView.as_view(), name='update_report'),
    path('delete/<int:pk>/', views.ReportDeleteView.as_view(), name='delete_report'),
    path('update-status/<int:pk>/', views.ReportUpdateStatusView.as_view(), name='update_status'),
]