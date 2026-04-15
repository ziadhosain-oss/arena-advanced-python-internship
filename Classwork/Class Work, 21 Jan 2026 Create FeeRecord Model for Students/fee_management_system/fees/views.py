from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Student, FeeRecord, FeePayment
from .forms import FeeRecordForm, FeePaymentForm, FeeFilterForm
from decimal import Decimal

@login_required
def dashboard(request):
    """Fee Management Dashboard"""
    # Statistics
    total_students = Student.objects.count()
    total_fees_due = FeeRecord.objects.aggregate(
        total=Sum('amount_due') - Sum('amount_paid')
    )['total'] or 0
    total_collected = FeeRecord.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    overdue_count = FeeRecord.objects.filter(
        status__in=['not_paid', 'partial'],
        due_date__lt=timezone.now().date()
    ).count()
    
    # Recent payments
    recent_payments = FeePayment.objects.select_related('fee_record__student').order_by('-payment_date')[:5]
    
    # Fee type summary
    fee_type_summary = FeeRecord.objects.values('fee_type').annotate(
        total_due=Sum('amount_due'),
        total_paid=Sum('amount_paid'),
        count=Count('id')
    )
    
    context = {
        'total_students': total_students,
        'total_fees_due': total_fees_due,
        'total_collected': total_collected,
        'overdue_count': overdue_count,
        'recent_payments': recent_payments,
        'fee_type_summary': fee_type_summary,
    }
    return render(request, 'fees/dashboard.html', context)

@login_required
def student_fee_list(request, student_id):
    """View all fee records for a student"""
    student = get_object_or_404(Student, id=student_id)
    fee_records = student.fee_records.all()
    
    # Calculate totals
    total_due = fee_records.aggregate(Sum('amount_due'))['amount_due__sum'] or 0
    total_paid = fee_records.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    total_balance = total_due - total_paid
    
    context = {
        'student': student,
        'fee_records': fee_records,
        'total_due': total_due,
        'total_paid': total_paid,
        'total_balance': total_balance,
    }
    return render(request, 'fees/student_fee_list.html', context)

@login_required
def all_fee_records(request):
    """View all fee records with filters"""
    fee_records = FeeRecord.objects.select_related('student', 'created_by').all()
    
    # Apply filters
    fee_type = request.GET.get('fee_type')
    status = request.GET.get('status')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    if fee_type:
        fee_records = fee_records.filter(fee_type=fee_type)
    if status:
        fee_records = fee_records.filter(status=status)
    if from_date:
        fee_records = fee_records.filter(due_date__gte=from_date)
    if to_date:
        fee_records = fee_records.filter(due_date__lte=to_date)
    
    # Pagination
    paginator = Paginator(fee_records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    form = FeeFilterForm(request.GET)
    
    context = {
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'fees/all_fee_records.html', context)

@login_required
def add_fee_record(request, student_id=None):
    """Add a new fee record"""
    student = None
    if student_id:
        student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = FeeRecordForm(request.POST)
        if form.is_valid():
            fee_record = form.save(commit=False)
            if student:
                fee_record.student = student
            fee_record.created_by = request.user
            fee_record.save()
            messages.success(request, f'Fee record added successfully for {fee_record.student.name}')
            return redirect('student_fee_list', student_id=fee_record.student.id)
    else:
        initial = {}
        if student:
            initial['student'] = student
        form = FeeRecordForm(initial=initial)
    
    return render(request, 'fees/add_fee_record.html', {
        'form': form,
        'student': student
    })

@login_required
def edit_fee_record(request, fee_record_id):
    """Edit a fee record"""
    fee_record = get_object_or_404(FeeRecord, id=fee_record_id)
    
    if request.method == 'POST':
        form = FeeRecordForm(request.POST, instance=fee_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee record updated successfully')
            return redirect('student_fee_list', student_id=fee_record.student.id)
    else:
        form = FeeRecordForm(instance=fee_record)
    
    return render(request, 'fees/edit_fee_record.html', {
        'form': form,
        'fee_record': fee_record
    })

@login_required
def delete_fee_record(request, fee_record_id):
    """Delete a fee record"""
    fee_record = get_object_or_404(FeeRecord, id=fee_record_id)
    student_id = fee_record.student.id
    if request.method == 'POST':
        fee_record.delete()
        messages.success(request, 'Fee record deleted successfully')
        return redirect('student_fee_list', student_id=student_id)
    
    return render(request, 'fees/delete_fee_record.html', {'fee_record': fee_record})

@login_required
def make_payment(request, fee_record_id):
    """Make a payment for a fee record"""
    fee_record = get_object_or_404(FeeRecord, id=fee_record_id)
    
    if request.method == 'POST':
        form = FeePaymentForm(request.POST, fee_record=fee_record)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.fee_record = fee_record
            payment.received_by = request.user
            payment.save()
            
            # Update fee record
            fee_record.make_payment(
                amount=payment.amount,
                transaction_id=payment.transaction_id,
                payment_method=payment.payment_method
            )
            
            messages.success(request, f'Payment of ₹{payment.amount:,.2f} received successfully')
            return redirect('student_fee_list', student_id=fee_record.student.id)
    else:
        form = FeePaymentForm(fee_record=fee_record)
    
    return render(request, 'fees/make_payment.html', {
        'form': form,
        'fee_record': fee_record
    })

@login_required
def overdue_fees(request):
    """View all overdue fees"""
    today = timezone.now().date()
    overdue_fees = FeeRecord.objects.filter(
        Q(status='not_paid') | Q(status='partial'),
        due_date__lt=today
    ).select_related('student')
    
    total_overdue = overdue_fees.aggregate(total=Sum('balance'))['total'] or 0
    
    # Group by class
    by_class = {}
    for fee in overdue_fees:
        class_name = fee.student.class_name
        if class_name not in by_class:
            by_class[class_name] = {'count': 0, 'total': 0}
        by_class[class_name]['count'] += 1
        by_class[class_name]['total'] += float(fee.balance)
    
    context = {
        'overdue_fees': overdue_fees,
        'total_overdue': total_overdue,
        'by_class': by_class,
        'today': today,
    }
    return render(request, 'fees/overdue_fees.html', context)

@login_required
def fee_summary(request):
    """Fee summary dashboard"""
    # Summary by fee type
    fee_type_summary = FeeRecord.objects.values('fee_type').annotate(
        total_due=Sum('amount_due'),
        total_paid=Sum('amount_paid'),
        total_balance=Sum('amount_due') - Sum('amount_paid'),
        count=Count('id')
    )
    
    # Summary by class
    class_summary = FeeRecord.objects.values('student__class_name').annotate(
        total_due=Sum('amount_due'),
        total_paid=Sum('amount_paid'),
        student_count=Count('student', distinct=True)
    )
    
    # Monthly collection
    monthly_collection = FeePayment.objects.values('payment_date__year', 'payment_date__month').annotate(
        total=Sum('amount')
    ).order_by('-payment_date__year', '-payment_date__month')[:12]
    
    # Recent payments
    recent_payments = FeePayment.objects.select_related('fee_record__student').order_by('-payment_date')[:10]
    
    context = {
        'fee_type_summary': fee_type_summary,
        'class_summary': class_summary,
        'monthly_collection': monthly_collection,
        'recent_payments': recent_payments,
    }
    return render(request, 'fees/fee_summary.html', context)