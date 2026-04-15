from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from decimal import Decimal

class Student(models.Model):
    """
    Student Model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    roll_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.roll_number})"
    
    class Meta:
        ordering = ['roll_number']


class FeeRecord(models.Model):
    """
    Fee Record Model for tracking student fees
    """
    
    # Fee Types Choices
    class FeeType(models.TextChoices):
        TUITION = 'tuition', 'Tuition Fee'
        EXAM = 'exam', 'Exam Fee'
        LIBRARY = 'library', 'Library Fee'
        OTHERS = 'others', 'Other Fees'
    
    # Payment Status Choices
    class PaymentStatus(models.TextChoices):
        PAID = 'paid', 'Paid'
        NOT_PAID = 'not_paid', 'Not Paid'
        PARTIAL = 'partial', 'Partially Paid'
        OVERDUE = 'overdue', 'Overdue'
    
    # Basic Information
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='fee_records',
        verbose_name='Student'
    )
    
    fee_type = models.CharField(
        max_length=20,
        choices=FeeType.choices,
        default=FeeType.TUITION,
        verbose_name='Fee Type'
    )
    
    # Amount Fields
    amount_due = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Amount Due'
    )
    
    amount_paid = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0,
        verbose_name='Amount Paid'
    )
    
    # Status Fields
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.NOT_PAID,
        verbose_name='Payment Status'
    )
    
    # Date Fields
    due_date = models.DateField(
        verbose_name='Due Date'
    )
    
    payment_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name='Payment Date'
    )
    
    # Additional Information
    description = models.TextField(
        blank=True,
        verbose_name='Description'
    )
    
    late_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0,
        verbose_name='Late Fee'
    )
    
    discount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0,
        verbose_name='Discount'
    )
    
    # Transaction Details
    transaction_id = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name='Transaction ID'
    )
    
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('cash', 'Cash'),
            ('card', 'Card'),
            ('bank_transfer', 'Bank Transfer'),
            ('online', 'Online Payment'),
            ('cheque', 'Cheque'),
        ],
        verbose_name='Payment Method'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='created_fee_records',
        verbose_name='Created By'
    )
    
    class Meta:
        ordering = ['-due_date', 'student__name']
        verbose_name = 'Fee Record'
        verbose_name_plural = 'Fee Records'
        indexes = [
            models.Index(fields=['student', 'fee_type']),
            models.Index(fields=['status', 'due_date']),
        ]
    
    def __str__(self):
        return f"{self.student.name} - {self.get_fee_type_display()} - {self.status}"
    
    @property
    def balance(self):
        """Calculate due amount / balance"""
        return self.amount_due - self.amount_paid
    
    @property
    def is_overdue(self):
        """Check if fee is overdue"""
        if self.status != self.PaymentStatus.PAID and date.today() > self.due_date:
            return True
        return False
    
    @property
    def payment_percentage(self):
        """Calculate payment percentage"""
        if self.amount_due > 0:
            return (self.amount_paid / self.amount_due) * 100
        return 0
    
    def update_status(self):
        """Automatically update status based on amount paid and due date"""
        if self.amount_paid >= self.amount_due:
            self.status = self.PaymentStatus.PAID
            self.payment_date = timezone.now().date()
        elif self.amount_paid > 0:
            self.status = self.PaymentStatus.PARTIAL
        elif self.is_overdue:
            self.status = self.PaymentStatus.OVERDUE
        else:
            self.status = self.PaymentStatus.NOT_PAID
        
        self.save(update_fields=['status', 'payment_date'])
    
    def make_payment(self, amount, transaction_id=None, payment_method=None):
        """Process a payment for this fee record"""
        if amount <= 0:
            raise ValueError("Payment amount must be greater than 0")
        
        if self.amount_paid >= self.amount_due:
            raise ValueError("Fee already fully paid")
        
        remaining = self.balance
        if amount > remaining:
            raise ValueError(f"Amount exceeds remaining balance of {remaining}")
        
        self.amount_paid += amount
        self.transaction_id = transaction_id or self.transaction_id
        self.payment_method = payment_method or self.payment_method
        
        # Update status
        self.update_status()
        
        return True
    
    def save(self, *args, **kwargs):
        """Override save to auto-update status and validate amounts"""
        # Ensure amount_paid doesn't exceed amount_due
        if self.amount_paid > self.amount_due:
            self.amount_paid = self.amount_due
        
        # Update status before saving
        if self.amount_paid >= self.amount_due:
            self.status = self.PaymentStatus.PAID
            if not self.payment_date:
                self.payment_date = timezone.now().date()
        elif self.is_overdue:
            self.status = self.PaymentStatus.OVERDUE
        elif self.amount_paid > 0:
            self.status = self.PaymentStatus.PARTIAL
        else:
            self.status = self.PaymentStatus.NOT_PAID
        
        super().save(*args, **kwargs)
    
    def get_fee_summary(self):
        """Get a summary of the fee record"""
        return {
            'fee_type': self.get_fee_type_display(),
            'amount_due': float(self.amount_due),
            'amount_paid': float(self.amount_paid),
            'balance': float(self.balance),
            'status': self.get_status_display(),
            'due_date': self.due_date,
            'is_overdue': self.is_overdue,
            'payment_percentage': round(self.payment_percentage, 2)
        }


class FeePayment(models.Model):
    """
    Separate model for tracking individual payments (for detailed history)
    """
    fee_record = models.ForeignKey(
        FeeRecord, 
        on_delete=models.CASCADE, 
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    remarks = models.TextField(blank=True)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment of {self.amount} for {self.fee_record}"
    
    class Meta:
        ordering = ['-payment_date']


class FeeStructure(models.Model):
    """
    Define standard fee structures for different classes
    """
    class_name = models.CharField(max_length=50)
    fee_type = models.CharField(max_length=20, choices=FeeRecord.FeeType.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_day_of_month = models.IntegerField(default=10)
    academic_year = models.CharField(max_length=9)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.class_name} - {self.get_fee_type_display()} - {self.academic_year}"
    
    class Meta:
        unique_together = ['class_name', 'fee_type', 'academic_year']