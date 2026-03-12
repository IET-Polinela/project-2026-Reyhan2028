from django.urls import path
from . import views

urlpatterns = [
    # Alamatnya kosong karena nanti sudah dipicu oleh /about/ di URL utama
    path('', views.about_page, name='about'),
]