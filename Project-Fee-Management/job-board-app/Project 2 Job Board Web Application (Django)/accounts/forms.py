from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import EmployerProfile, SeekerProfile, User


class EmployerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    company_name = forms.CharField(max_length=200)
    website = forms.URLField(required=False)
    location = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'company_name', 'website', 'location', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.is_employer = True
        if commit:
            user.save()
            EmployerProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                website=self.cleaned_data.get('website', ''),
                location=self.cleaned_data['location'],
            )
        return user


class SeekerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    resume = forms.FileField(required=True)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'resume', 'bio', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.is_seeker = True
        if commit:
            user.save()
            SeekerProfile.objects.create(
                user=user,
                resume=self.cleaned_data['resume'],
                bio=self.cleaned_data.get('bio', ''),
            )
        return user
