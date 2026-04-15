from django import forms
from .models import FeeRecord, FeePayment
from django.utils import timezone

class FeeRecordForm(forms.ModelForm):
    class Meta:
        model = FeeRecord
        fields = [
            'student', 'fee_type', 'amount_due', 'due_date', 
            'description', 'discount', 'late_fee'
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'amount_due': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'late_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].widget.attrs.update({'class': 'form-control'})
        self.fields['fee_type'].widget.attrs.update({'class': 'form-control'})
    
    def clean_amount_due(self):
        amount = self.cleaned_data.get('amount_due')
        if amount <= 0:
            raise forms.ValidationError("Amount due must be greater than 0")
        return amount
    
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError("Due date cannot be in the past")
        return due_date

class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['amount', 'payment_method', 'transaction_id', 'remarks']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.fee_record = kwargs.pop('fee_record', None)
        super().__init__(*args, **kwargs)
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if self.fee_record and amount > self.fee_record.balance:
            raise forms.ValidationError(
                f"Amount cannot exceed remaining balance: ₹{self.fee_record.balance:,.2f}"
            )
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0")
        return amount

class FeeFilterForm(forms.Form):
    fee_type = forms.ChoiceField(
        choices=[('', 'All')] + FeeRecord.FeeType.choices,
        required=False
    )
    status = forms.ChoiceField(
        choices=[('', 'All')] + FeeRecord.PaymentStatus.choices,
        required=False
    )
    from_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    to_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )