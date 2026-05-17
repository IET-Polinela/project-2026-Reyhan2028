from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(viewsets.ModelViewSet):
    # Mengatur agar API dapat diakses oleh siapa saja untuk keperluan pengujian
    permission_classes = [permissions.AllowAny]
    
    # Mengambil semua data dari model Report
    queryset = Report.objects.all()
    
    # Menghubungkan ViewSet ini dengan serializer yang sudah kita buat sebelumnya
    serializer_class = ReportSerializer