from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    # c. Melakukan override field reporter agar identitas pelapor anonim
    reporter = serializers.SerializerMethodField()

    class Meta:
        model = Report
        # b. Mengaitkan serializer dengan model Report dan menentukan field yang ditampilkan
        fields = [
            'id', 'title', 'category', 'description', 
            'location', 'status', 'reporter', 
            'created_at', 'updated_at'
        ]

    # Fungsi untuk menghasilkan string statis "Warga Anonim" pada field reporter
    def get_reporter(self, obj):
        return "Warga Anonim"