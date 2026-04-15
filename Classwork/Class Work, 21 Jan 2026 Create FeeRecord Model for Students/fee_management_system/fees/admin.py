from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Student, FeeRecord, FeePayment, FeeStructure

class FeeRecordInline(admin.TabularInline):
    model = FeeRecord
    extra = 0
    fields = ['fee_type', 'amount_due', 'amount_paid', 'balance', 'status', 'due_date']
    readonly_fields = ['balance']
    
    def balance(self, obj):
        return f"₹{obj.balance:,.2f}"
    balance.short_description = 'Balance'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'class_name', 'section', 'phone', 'total_fees_due', 'view_fees_link']
    list_filter = ['class_name', 'section']
    search_fields = ['roll_number', 'name', 'email']
    inlines = [FeeRecordInline]
    
    def total_fees_due(self, obj):
        total_due = sum(fee.balance for fee in obj.fee_records.all())
        color = 'red' if total_due > 0 else 'green'
        return format_html(f'<span style="color: {color};">₹{total_due:,.2f}</span>')
    total_fees_due.short_description = 'Total Fees Due'
    
    def view_fees_link(self, obj):
        url = reverse('admin:fees_feerecord_changelist') + f'?student__id__exact={obj.id}'
        return format_html(f'<a href="{url}">View Fees</a>')
    view_fees_link.short_description = 'Fee Records'

@admin.register(FeeRecord)
class FeeRecordAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'fee_type', 'amount_due', 'amount_paid', 
        'balance_display', 'status_colored', 'due_date', 'payment_status'
    ]
    list_filter = ['fee_type', 'status', 'due_date', 'student__class_name']
    search_fields = ['student__name', 'student__roll_number', 'transaction_id']
    readonly_fields = ['balance', 'payment_percentage']
    list_editable = ['amount_paid']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student', 'fee_type')
        }),
        ('Amount Details', {
            'fields': ('amount_due', 'amount_paid', 'discount', 'late_fee')
        }),
        ('Payment Information', {
            'fields': ('status', 'due_date', 'payment_date', 'transaction_id', 'payment_method')
        }),
        ('Additional Information', {
            'fields': ('description', 'created_by'),
            'classes': ('collapse',)
        })
    )
    
    def balance_display(self, obj):
        balance = obj.balance
        color = 'red' if balance > 0 else 'green'
        return format_html(f'<span style="color: {color}; font-weight: bold;">₹{balance:,.2f}</span>')
    balance_display.short_description = 'Balance'
    
    def status_colored(self, obj):
        colors = {
            'paid': 'green',
            'not_paid': 'red',
            'partial': 'orange',
            'overdue': 'darkred'
        }
        color = colors.get(obj.status, 'black')
        return format_html(f'<span style="color: {color}; font-weight: bold;">{obj.get_status_display()}</span>')
    status_colored.short_description = 'Status'
    
    def payment_percentage(self, obj):
        return f"{obj.payment_percentage:.1f}%"
    payment_percentage.short_description = 'Payment %'
    
    def payment_status(self, obj):
        if obj.status == 'paid':
            return format_html('✅ Fully Paid')
        elif obj.status == 'partial':
            return format_html('⚠️ Partially Paid')
        elif obj.is_overdue:
            return format_html('❌ Overdue')
        else:
            return format_html('⏳ Pending')
    payment_status.short_description = 'Payment Status'
    
    actions = ['mark_as_paid', 'send_reminder']
    
    def mark_as_paid(self, request, queryset):
        for fee in queryset:
            fee.amount_paid = fee.amount_due
            fee.save()
        self.message_user(request, f"{queryset.count()} fee records marked as paid.")
    mark_as_paid.short_description = "Mark selected as paid"
    
    def send_reminder(self, request, queryset):
        self.message_user(request, f"Reminders sent for {queryset.count()} fee records.")
    send_reminder.short_description = "Send payment reminder"

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['fee_record', 'amount', 'payment_date', 'transaction_id', 'payment_method']
    list_filter = ['payment_method', 'payment_date']
    search_fields = ['fee_record__student__name', 'transaction_id']
    readonly_fields = ['created_at']

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'fee_type', 'amount', 'academic_year', 'is_active']
    list_filter = ['class_name', 'fee_type', 'academic_year', 'is_active']
    search_fields = ['class_name']
    list_editable = ['amount', 'is_active']