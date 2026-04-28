from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# Tambahkan import untuk proteksi login
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Report

# 1. Dashboard / Halaman Utama
class IndexView(View):
    def get(self, request):
        return render(request, 'main_app/index.html')

# 2. Daftar Semua Laporan (Akses: Semua User)
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'
    ordering = ['-created_at']

# 3. Detail Satu Laporan (Akses: Semua User)
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'

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
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak! Hanya Admin yang boleh menambah laporan.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

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
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak! Anda tidak memiliki izin mengedit data.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

# 6. Hapus Laporan (Akses: Hanya Admin)
class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Silakan login terlebih dahulu.")
            return redirect('login')
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak! Hanya Admin yang bisa menghapus laporan.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Laporan telah berhasil dihapus.")
        return super().delete(request, *args, **kwargs)

# 7. Workflow: Update Status Laporan (Akses: Hanya Admin)
class ReportUpdateStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_admin:
            messages.error(request, "Hanya Admin yang dapat mengubah status laporan.")
            return redirect('home')
            
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        
        messages.success(request, f"Status '{report.title}' kini: {report.get_status_display()}!")
        return redirect('home')