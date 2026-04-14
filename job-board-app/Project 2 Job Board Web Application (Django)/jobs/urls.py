from django.urls import path

from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/jobs/new/', views.job_create, name='job_create'),
    path('employer/jobs/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('employer/jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('applications/<int:pk>/review/', views.application_review, name='application_review'),
]
