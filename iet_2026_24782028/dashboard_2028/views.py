from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count
from main_app.models import Report # Pastikan ini sesuai nama app laporanmu

# 1. View untuk menampilkan halaman Dashboard (HTML)
class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

# 2. View khusus untuk menyediakan data JSON (API)
def dashboard_data(request):
    # Menghitung distribusi status laporan
    status_distribution = list(Report.objects.values('status').annotate(total=Count('status')))
    
    # Menghitung distribusi kategori laporan
    category_distribution = list(Report.objects.values('category').annotate(total=Count('category')))
    
    # Mengambil 5 laporan terbaru (REPORTED)
    recent_reports = list(Report.objects.filter(status='REPORTED').order_by('-id')[:5].values(
        'title', 'category', 'status', 'location'
    ))
    
    # Mengambil 5 laporan selesai terbaru (RESOLVED)
    resolved_reports = list(Report.objects.filter(status='RESOLVED').order_by('-id')[:5].values(
        'title', 'category', 'status', 'location'
    ))

    # Mengembalikan data dalam format JSON
    return JsonResponse({
        'status_data': status_distribution,
        'category_data': category_distribution,
        'recent_reports': recent_reports,
        'resolved_reports': resolved_reports,
    })