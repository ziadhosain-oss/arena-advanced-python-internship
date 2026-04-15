from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to SisApp 2026</h1><p><a href='/about/'>About Us</a></p>")

def about(request):
    return render(request, 'public_site/about.html')
