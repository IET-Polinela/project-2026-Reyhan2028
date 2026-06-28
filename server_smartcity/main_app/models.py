from django.db import models
from django.conf import settings # Tambahkan ini untuk relasi ke CustomUser

class Report(models.Model):
    # a. Menambahkan nilai “DRAFT” ke dalam pilihan status laporan
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'), # Tambahan baru sesuai Lab 9
        ('REPORTED', 'Reported'),
        ('VERIFIED', 'Verified'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    
    # b. Menambahkan field reporter (ForeignKey ke CustomUser)
    # Ini penting agar Citizen bisa mengelola laporan mereka sendiri
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='reports',
        null=True, # null=True agar data lama tidak error saat migrasi
        blank=True
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='REPORTED'
    )
    
    # c. Field created_at (sudah ada) dan updated_at (baru)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # Tambahkan ini untuk rekam jejak waktu ubah

    def __str__(self):
        return self.title