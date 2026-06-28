from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    # c. Melakukan override field reporter agar identitas pelapor anonim
    reporter = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        # b. Mengaitkan serializer dengan model Report dan menentukan field yang ditampilkan
        fields = [
            'id', 'title', 'category', 'description', 
            'location', 'status', 'reporter', 
            'created_at', 'updated_at', 'is_owner'
        ]

    # Fungsi untuk menghasilkan string statis "Warga Anonim" pada field reporter
    def get_reporter(self, obj):
        return "Warga Anonim"

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.reporter_id == request.user.id
