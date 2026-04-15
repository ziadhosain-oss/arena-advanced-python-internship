from django import forms

from .models import Application, Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume']
        labels = {
            'resume': 'Resume Upload',
        }
