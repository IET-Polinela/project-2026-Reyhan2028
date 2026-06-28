from rest_framework import permissions

class IsOwnerAndDraftOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Jika request adalah GET, HEAD, atau OPTIONS, izinkan akses (Read-Only)
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Untuk operasi menulis (PUT, PATCH, DELETE), pastikan pelapor adalah user yang login 
        # DAN status laporan masih berstatus 'DRAFT'
        return obj.reporter == request.user and obj.status == 'DRAFT'