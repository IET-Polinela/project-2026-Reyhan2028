from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'category', 'description', 'location']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg', 
                'placeholder': 'Apa masalah yang ingin dilaporkan?'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select form-select-lg'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Berikan detail laporan Anda secara lengkap...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Contoh: Gedung Sakura, Lantai 2'
            }),
        }