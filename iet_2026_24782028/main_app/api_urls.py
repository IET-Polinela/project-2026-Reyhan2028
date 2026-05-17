from rest_framework.routers import DefaultRouter
from .api_views import ReportViewSet

# b. Gunakan DefaultRouter dan registrasi ReportViewSet
router = DefaultRouter()
router.register(r'report', ReportViewSet, basename='report')

# c. urlpatterns otomatis dari router
urlpatterns = router.urls