from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Report

# a. ListView menggantikan fungsi home
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html' # Menggunakan template home.html kamu
    context_object_name = 'reports'
    ordering = ['-created_at']

# b. DetailView untuk melihat detail satu laporan
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'

# c. CreateView menggantikan fungsi add_report
class ReportCreateView(CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('home')

# d. UpdateView menggantikan fungsi update_report
class ReportUpdateView(UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('home')

# e. DeleteView menggantikan fungsi delete_report
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/delete_confirm.html'
    success_url = reverse_lazy('home')

# Fitur Baru: View khusus untuk perubahan status workflow (Halaman 2 Lab 4)
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        report.status = new_status
        report.save()
        return redirect('home')