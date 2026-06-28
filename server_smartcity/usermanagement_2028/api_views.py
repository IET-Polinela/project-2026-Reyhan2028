from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    # Mengizinkan siapa saja untuk mengakses rute pendaftaran ini tanpa token login
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer