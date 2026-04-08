from django.db import models

class Report(models.Model):
    # Pilihan status laporan sesuai instruksi Lab 4
    STATUS_CHOICES = [
        ('REPORTED', 'Reported'),
        ('VERIFIED', 'Verified'), # Tambahan status baru
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    
    # Field status dengan default 'REPORTED'
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='REPORTED'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title