from django.urls import path
from . import views

app_name = 'fees'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Student fee management
    path('student/<int:student_id>/fees/', views.student_fee_list, name='student_fee_list'),
    path('student/<int:student_id>/add-fee/', views.add_fee_record, name='add_fee_record'),
    
    # Fee record management
    path('fee-records/', views.all_fee_records, name='all_fee_records'),
    path('fee-record/add/', views.add_fee_record, name='add_fee_record_general'),
    path('fee-record/<int:fee_record_id>/edit/', views.edit_fee_record, name='edit_fee_record'),
    path('fee-record/<int:fee_record_id>/delete/', views.delete_fee_record, name='delete_fee_record'),
    path('fee-record/<int:fee_record_id>/pay/', views.make_payment, name='make_payment'),
    
    # Reports
    path('overdue/', views.overdue_fees, name='overdue_fees'),
    path('summary/', views.fee_summary, name='fee_summary'),
]