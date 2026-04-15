from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Teacher

class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'Teacher Profile'
    fk_name = 'user'
    fieldsets = (
        ('Teacher Information', {
            'fields': ('teacher_id', 'teacher_type', 'department', 'qualification')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address')
        }),
        ('Status', {
            'fields': ('joining_date', 'is_active')
        }),
        ('Permissions', {
            'fields': ('permissions',),
            'classes': ('collapse',)
        }),
    )

class CustomUserAdmin(UserAdmin):
    inlines = (TeacherInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_teacher_type', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'teacher_profile__teacher_type')
    
    def get_teacher_type(self, obj):
        if hasattr(obj, 'teacher_profile'):
            return obj.teacher_profile.get_teacher_type_display()
        return 'Not a Teacher'
    get_teacher_type.short_description = 'Teacher Type'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'get_user_name', 'teacher_type', 'department', 'is_active')
    list_filter = ('teacher_type', 'department', 'is_active')
    search_fields = ('teacher_id', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Mapping', {
            'fields': ('user', 'teacher_id')
        }),
        ('Teacher Details', {
            'fields': ('teacher_type', 'department', 'qualification', 'joining_date')
        }),
        ('Contact', {
            'fields': ('phone_number', 'address')
        }),
        ('Permissions', {
            'fields': ('permissions', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_user_name.short_description = 'Name'
    get_user_name.admin_order_field = 'user__first_name'
