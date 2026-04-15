from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm, JobForm
from .models import Application, Job


def home(request):
    search_text = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()
    salary = request.GET.get('salary', '').strip()

    jobs = Job.objects.select_related('category', 'employer').order_by('-created_at')

    if search_text:
        jobs = jobs.filter(
            Q(title__icontains=search_text)
            | Q(description__icontains=search_text)
            | Q(category__name__icontains=search_text)
        )

    if location:
        jobs = jobs.filter(location__icontains=location)

    if salary.isdigit():
        jobs = jobs.filter(salary__gte=int(salary))

    paginator = Paginator(jobs, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'jobs/home.html', {
        'page_obj': page_obj,
        'search_text': search_text,
        'location': location,
        'salary': salary,
    })


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    already_applied = False

    if request.user.is_authenticated and request.user.is_seeker:
        already_applied = Application.objects.filter(job=job, seeker=request.user).exists()

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'already_applied': already_applied,
    })


@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if not request.user.is_seeker:
        messages.error(request, 'Only job seekers can apply for open roles.')
        return redirect('jobs:job_detail', pk=job.pk)

    if Application.objects.filter(job=job, seeker=request.user).exists():
        messages.info(request, 'You have already applied for this job.')
        return redirect('jobs:job_detail', pk=job.pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.seeker = request.user
            application.save()
            messages.success(request, 'Your application has been submitted successfully.')
            return redirect('jobs:job_detail', pk=job.pk)
    else:
        form = ApplicationForm()

    return render(request, 'jobs/apply.html', {'job': job, 'form': form})


@login_required
def employer_dashboard(request):
    if not request.user.is_employer:
        messages.error(request, 'Only employers can access the dashboard.')
        return redirect('jobs:home')

    jobs = request.user.jobs.order_by('-created_at')
    applications = Application.objects.filter(job__employer=request.user).select_related('job', 'seeker').order_by('-applied_at')

    return render(request, 'jobs/employer_dashboard.html', {
        'jobs': jobs,
        'applications': applications,
    })


@login_required
def job_create(request, pk=None):
    if not request.user.is_employer:
        messages.error(request, 'Only employers can post jobs.')
        return redirect('jobs:home')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job posted successfully.')
            return redirect('jobs:employer_dashboard')
    else:
        form = JobForm()

    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Post a New Job'})


@login_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully.')
            return redirect('jobs:employer_dashboard')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Edit Job'})


@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('jobs:employer_dashboard')

    return render(request, 'jobs/confirm_delete.html', {'job': job})


@login_required
def application_review(request, pk):
    application = get_object_or_404(Application, pk=pk, job__employer=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action in ['accepted', 'rejected']:
            application.status = action
            application.save()

            if application.seeker.email:
                send_mail(
                    f'Your application has been {action}',
                    f'Hello {application.seeker.username},\n\nYour application for "{application.job.title}" has been {action}.',
                    settings.DEFAULT_FROM_EMAIL,
                    [application.seeker.email],
                )

            messages.success(request, f'Application has been marked {action}.')
            return redirect('jobs:employer_dashboard')

    return render(request, 'jobs/application_review.html', {'application': application})
