from django.shortcuts import render

def home(request):
    return render(request, 'hero_page/landing_page.html')
