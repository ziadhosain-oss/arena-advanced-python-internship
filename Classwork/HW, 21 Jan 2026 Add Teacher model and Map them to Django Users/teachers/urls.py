from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('dashboard/', views.TeacherDashboardView.as_view(), name='dashboard'),
    path('attendance/', views.view_attendance, name='view_attendance_all'),
    path('attendance/<int:student_id>/', views.view_attendance, name='view_attendance'),
    path('marks/', views.view_marks, name='view_marks_all'),
    path('marks/<int:student_id>/', views.view_marks, name='view_marks'),
    path('fees/', views.view_fees, name='view_fees_all'),
    path('fees/<int:student_id>/', views.view_fees, name='view_fees'),
    path('manage-students/', views.manage_students, name='manage_students'),
]
