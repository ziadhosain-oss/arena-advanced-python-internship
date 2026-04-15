from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # Add this import

urlpatterns = [
    path('', lambda request: redirect('admin/')),  # Add this line
    path('admin/', admin.site.urls),
    path('fees/', include('fees.urls')),
]