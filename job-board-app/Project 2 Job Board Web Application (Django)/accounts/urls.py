from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_choice, name='signup_choice'),
    path('signup/employer/', views.employer_signup, name='employer_signup'),
    path('signup/seeker/', views.seeker_signup, name='seeker_signup'),
]
