from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import EmployerSignUpForm, SeekerSignUpForm


def signup_choice(request):
    return render(request, 'accounts/signup_choice.html')


def employer_signup(request):
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Employer account created successfully.')
            return redirect('jobs:employer_dashboard')
    else:
        form = EmployerSignUpForm()

    return render(request, 'accounts/signup_form.html', {
        'form': form,
        'title': 'Employer Sign Up',
    })


def seeker_signup(request):
    if request.method == 'POST':
        form = SeekerSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Job seeker account created successfully.')
            return redirect('jobs:home')
    else:
        form = SeekerSignUpForm()

    return render(request, 'accounts/signup_form.html', {
        'form': form,
        'title': 'Job Seeker Sign Up',
    })
