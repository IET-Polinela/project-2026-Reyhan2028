from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report # [cite: 63, 64]
        fields = ['title', 'category', 'description', 'location'] # [cite: 65, 66]