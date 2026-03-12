from django.urls import path
from . import views # Di sini baru benar pakai 'from . import views' karena file views.py ada di folder yang sama [cite: 19]

urlpatterns = [
    path('', views.home, name='home'),
]