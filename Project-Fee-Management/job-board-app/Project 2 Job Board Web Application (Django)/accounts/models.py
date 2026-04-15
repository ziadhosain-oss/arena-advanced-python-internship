from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # These flags determine the user's role
    is_employer = models.BooleanField(default=False)
    is_seeker = models.BooleanField(default=False)
    
    # Common field for both roles
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

class SeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seeker_profile')
    resume = models.FileField(upload_to='resumes/')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username