from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer
# --- TAMBAHAN UPDATE LAB 10 (Impor permission buatan kita) ---
from .permissions import IsOwnerAndDraftOrReadOnly 

class ReportViewSet(viewsets.ModelViewSet):
    # Mengambil semua data dari model Report (Tetap dipertahankan)
    queryset = Report.objects.all()
    
    # Menghubungkan ViewSet ini dengan serializer (Tetap dipertahankan)
    serializer_class = ReportSerializer

    # --- TAMBAHAN UPDATE LAB 10 (Menggantikan AllowAny lama) ---
    def get_permissions(self):
        # Operasi ubah (PUT/PATCH) dan hapus (DELETE) hanya untuk pemilik berstatus DRAFT
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerAndDraftOrReadOnly()]
        # Operasi lainnya (GET list/detail, POST) hanya mewajibkan pengguna sudah login menggunakan JWT
        return [permissions.IsAuthenticated()]

    # --- TAMBAHAN UPDATE LAB 10 (Otomatis mencatat siapa pelapornya) ---
    def perform_create(self, serializer):
        # Mengisi field reporter secara otomatis berdasarkan token warga yang sedang login
        serializer.save(reporter=self.request.user)