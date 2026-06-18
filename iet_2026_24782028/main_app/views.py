from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Report

# --- IMPORT UNTUK LAB 7 ---
from django.http import JsonResponse

# 1. Dashboard / Halaman Utama
class IndexView(View):
    def get(self, request):
        return render(request, 'main_app/index.html')

# 2. Daftar Semua Laporan (Akses: Semua User)
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return Report.objects.exclude(status='DRAFT').order_by('-created_at')

# 3. Detail Satu Laporan (Akses: Semua User)
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        return Report.objects.exclude(status='DRAFT')

# 4. Tambah Laporan Baru (Akses: Hanya Admin)
class ReportCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('home')
    success_message = "Laporan berhasil dibuat!"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Silakan login terlebih dahulu.")
            return redirect('login')
        messages.error(request, "Admin hanya dapat melihat dan memverifikasi laporan warga.")
        return redirect('home')

# 5. Edit Laporan (Akses: Hanya Admin)
class ReportUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('home')
    success_message = "Laporan berhasil diperbarui!"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Silakan login terlebih dahulu.")
            return redirect('login')
        messages.error(request, "Laporan warga tidak boleh diedit melalui halaman admin.")
        return redirect('home')

# 6. Hapus Laporan (Akses: Hanya Admin)
class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Silakan login terlebih dahulu.")
            return redirect('login')
        messages.error(request, "Laporan warga tidak boleh dihapus melalui halaman admin.")
        return redirect('home')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Laporan telah berhasil dihapus.")
        return super().delete(request, *args, **kwargs)

# 7. Workflow: Update Status Laporan (Akses: Hanya Admin)
class ReportUpdateStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_admin:
            messages.error(request, "Hanya Admin yang dapat mengubah status laporan.")
            return redirect('home')
            
        report = get_object_or_404(Report.objects.exclude(status='DRAFT'), pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        
        messages.success(request, f"Status '{report.title}' kini: {report.get_status_display()}!")
        return redirect('home')

# --- OPTIMASI LAB SESSION 7 ---

# 8. Fungsi untuk Live Search (DIPERBAIKI AGAR RINGAN)
def report_search(request):
    query = request.GET.get('q', '')
    
    # Jangan cari jika kurang dari 2 huruf
    if len(query) < 2:
        return JsonResponse({'reports': []})
    
    # Ambil kolom penting saja & batasi 10 hasil agar tidak lag
    reports = Report.objects.exclude(status='DRAFT').filter(
        title__icontains=query
    ).only('id', 'title', 'category', 'location', 'status')[:10]
    
    results = []
    for r in reports:
        results.append({
            'id': r.pk,
            'title': r.title,
            'category': r.category,
            'location': r.location,
            'status': r.get_status_display(),
        })
    return JsonResponse({'reports': results})

# 9. Fungsi untuk Detail Modal via AJAX
def report_detail_api(request, pk): 
    report = get_object_or_404(Report.objects.exclude(status='DRAFT'), pk=pk)
    data = {
        'title': report.title,
        'category': report.category,
        'description': report.description,
        'location': report.location,
        'status': report.get_status_display(),
    }
    return JsonResponse(data)
