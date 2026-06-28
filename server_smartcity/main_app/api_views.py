from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Report
from .serializers import ReportSerializer
# --- TAMBAHAN UPDATE LAB 10 (Impor permission buatan kita) ---
from .permissions import IsOwnerAndDraftOrReadOnly 

class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ReportViewSet(viewsets.ModelViewSet):
    # Menghubungkan ViewSet ini dengan serializer (Tetap dipertahankan)
    serializer_class = ReportSerializer
    pagination_class = ReportPagination

    def get_queryset(self):
        queryset = Report.objects.select_related('reporter').all().order_by('-updated_at')
        tab = self.request.query_params.get('tab')

        if tab == 'my_reports':
            queryset = queryset.filter(reporter=self.request.user)
        elif tab == 'feed':
            queryset = queryset.exclude(reporter=self.request.user).exclude(status='DRAFT')

        return queryset

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
