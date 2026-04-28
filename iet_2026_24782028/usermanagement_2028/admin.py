from django.contrib import admin
from .models import User

# Pengaturan tampilan untuk model User
class UserAdmin(admin.ModelAdmin):
    # Ini yang akan membuat kolom is_admin dan is_member muncul di daftar
    list_display = ('username', 'email', 'is_admin', 'is_member', 'is_staff')
    
    # Menambahkan filter di samping kanan untuk memudahkan pencarian
    list_filter = ('is_admin', 'is_member', 'is_staff')
    
    # Mengatur tampilan form saat kamu mengklik salah satu user
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informasi Pribadi', {'fields': ('email',)}),
        ('Status Hak Akses', {'fields': ('is_admin', 'is_member', 'is_staff', 'is_active', 'is_superuser')}),
    )

# Daftarkan model User dengan pengaturan UserAdmin di atas
admin.site.register(User, UserAdmin)