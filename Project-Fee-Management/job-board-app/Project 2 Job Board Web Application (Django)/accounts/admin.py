from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmployerProfile, SeekerProfile

# This makes our custom fields (is_employer, is_seeker) visible in the admin
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_employer', 'is_seeker', 'phone_number')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(EmployerProfile)
admin.site.register(SeekerProfile)