from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Teacher(models.Model):
    """Teacher model mapped to Django User"""
    
    # Teacher Types
    CLASS_TEACHER = 'CT'
    SUBJECT_TEACHER = 'ST'
    SUPERVISOR = 'SV'
    PRINCIPAL = 'PR'
    
    TEACHER_TYPE_CHOICES = [
        (CLASS_TEACHER, 'Class Teacher'),
        (SUBJECT_TEACHER, 'Subject Teacher'),
        (SUPERVISOR, 'Supervisor'),
        (PRINCIPAL, 'Principal'),
    ]
    
    # Permissions for RBAC
    CAN_VIEW_ATTENDANCE = 'view_attendance'
    CAN_EDIT_ATTENDANCE = 'edit_attendance'
    CAN_VIEW_MARKS = 'view_marks'
    CAN_EDIT_MARKS = 'edit_marks'
    CAN_VIEW_FEES = 'view_fees'
    CAN_EDIT_FEES = 'edit_fees'
    CAN_MANAGE_STUDENTS = 'manage_students'
    
    # Link to Django User
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    
    # Teacher specific fields
    teacher_id = models.CharField(max_length=20, unique=True)
    teacher_type = models.CharField(
        max_length=2,
        choices=TEACHER_TYPE_CHOICES,
        default=SUBJECT_TEACHER
    )
    department = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=200, blank=True)
    joining_date = models.DateField(default=timezone.now)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Role-based permissions (JSON field for flexible RBAC)
    permissions = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'teachers'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
        permissions = [
            ("can_manage_all_teachers", "Can manage all teachers"),
            ("can_view_all_students", "Can view all students"),
            ("can_access_all_records", "Can access all student records"),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.teacher_id})"
    
    def get_permissions_list(self):
        """Get list of permissions for this teacher based on teacher_type"""
        default_permissions = {
            self.CLASS_TEACHER: {
                self.CAN_VIEW_ATTENDANCE: True,
                self.CAN_EDIT_ATTENDANCE: True,
                self.CAN_VIEW_MARKS: True,
                self.CAN_EDIT_MARKS: False,
                self.CAN_VIEW_FEES: True,
                self.CAN_EDIT_FEES: False,
                self.CAN_MANAGE_STUDENTS: True,
            },
            self.SUBJECT_TEACHER: {
                self.CAN_VIEW_ATTENDANCE: True,
                self.CAN_EDIT_ATTENDANCE: True,
                self.CAN_VIEW_MARKS: True,
                self.CAN_EDIT_MARKS: True,
                self.CAN_VIEW_FEES: False,
                self.CAN_EDIT_FEES: False,
                self.CAN_MANAGE_STUDENTS: False,
            },
            self.SUPERVISOR: {
                self.CAN_VIEW_ATTENDANCE: True,
                self.CAN_EDIT_ATTENDANCE: False,
                self.CAN_VIEW_MARKS: True,
                self.CAN_EDIT_MARKS: False,
                self.CAN_VIEW_FEES: True,
                self.CAN_EDIT_FEES: False,
                self.CAN_MANAGE_STUDENTS: True,
            },
            self.PRINCIPAL: {
                self.CAN_VIEW_ATTENDANCE: True,
                self.CAN_EDIT_ATTENDANCE: True,
                self.CAN_VIEW_MARKS: True,
                self.CAN_EDIT_MARKS: True,
                self.CAN_VIEW_FEES: True,
                self.CAN_EDIT_FEES: True,
                self.CAN_MANAGE_STUDENTS: True,
            },
        }
        return default_permissions.get(self.teacher_type, {})
    
    def has_permission(self, permission):
        """Check if teacher has specific permission"""
        if not self.permissions:
            self.permissions = self.get_permissions_list()
            self.save()
        return self.permissions.get(permission, False)
    
    def save(self, *args, **kwargs):
        if not self.permissions:
            self.permissions = self.get_permissions_list()
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    """Auto-create Teacher profile when User is created with teacher flag"""
    if created and hasattr(instance, 'is_teacher'):
        Teacher.objects.get_or_create(
            user=instance,
            defaults={'teacher_id': f"TCH{instance.id:05d}"}
        )

@receiver(post_save, sender=User)
def save_teacher_profile(sender, instance, **kwargs):
    if hasattr(instance, 'teacher_profile'):
        instance.teacher_profile.save()
