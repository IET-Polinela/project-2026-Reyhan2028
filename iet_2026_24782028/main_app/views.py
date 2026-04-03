from django.shortcuts import render, redirect, get_object_or_404
from .models import Report
from .forms import ReportForm

# READ: Menampilkan semua laporan
def home(request):
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'main_app/home.html', {'reports': reports})

# CREATE: Menambah laporan baru
def add_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReportForm()
    
    # PASTIKAN BARIS INI SEJAJAR DENGAN 'if' DI ATAS
    return render(request, 'main_app/add_report.html', {'form': form})

# UPDATE: Mengedit laporan
def update_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReportForm(instance=report)
    
    # PASTIKAN BARIS INI SEJAJAR DENGAN 'if' DI ATAS
    return render(request, 'main_app/add_report.html', {'form': form, 'edit_mode': True})

# DELETE: Menghapus laporan
def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == "POST":
        report.delete()
        return redirect('home')
    
    # PASTIKAN BARIS INI SEJAJAR DENGAN 'if' DI ATAS
    return render(request, 'main_app/delete_confirm.html', {'report': report})