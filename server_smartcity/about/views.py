from django.shortcuts import render

def about_page(request):
    # Mengarahkan ke file about.html di folder templates/about/
    return render(request, 'about/about.html')