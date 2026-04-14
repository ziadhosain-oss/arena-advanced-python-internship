from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    student_name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}), 
        required=False
    )

    class Meta:
        model = Attendance
        fields = ['student', 'is_present']
        widgets = {
            'student': forms.HiddenInput(),
        }