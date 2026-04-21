from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import Report

# 1. Dashboard / Halaman Utama (Penyambutan)
class IndexView(View):
    def get(self, request):
        return render(request, 'main_app/index.html')

# 2. Daftar Semua Laporan (Halaman Reports)
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'
    ordering = ['-created_at']

# 3. Detail Satu Laporan
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'

# 4. Tambah Laporan Baru (Dengan Pesan Sukses)
class ReportCreateView(SuccessMessageMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('home')
    success_message = "Laporan berhasil dibuat!"

# 5. Edit Laporan (Dengan Pesan Sukses)
class ReportUpdateView(SuccessMessageMixin, UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('home')
    success_message = "Laporan berhasil diperbarui!"

# 6. Hapus Laporan
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('home')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Laporan telah berhasil dihapus.")
        return super().delete(request, *args, **kwargs)

# 7. Workflow: Update Status Laporan
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        
        # Pesan sukses dinamis
        messages.success(request, f"Status '{report.title}' kini: {report.get_status_display()}!")
        return redirect('home')