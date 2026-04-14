from django.contrib import admin
from django.urls import path
from students.views import mark_attendance, student_dashboard, export_performance_excel, export_performance_csv

urlpatterns = [
    path('', student_dashboard, name='home'),
    path('admin/', admin.site.urls),
    path('attendance/', mark_attendance, name='mark_attendance'),
    path('dashboard/', student_dashboard, name='dashboard'),
    path('export/excel/', export_performance_excel, name='export_excel'),
    path('export/csv/', export_performance_csv, name='export_csv'),
]