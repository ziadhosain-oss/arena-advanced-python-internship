from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .models import Teacher

def is_teacher(user):
    """Check if user is a teacher"""
    return hasattr(user, 'teacher_profile') and user.teacher_profile.is_active

def has_permission(permission_needed):
    """Decorator factory for checking teacher permissions"""
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if not is_teacher(request.user):
                return HttpResponseForbidden("Access Denied: Not a teacher")
            
            teacher = request.user.teacher_profile
            if not teacher.has_permission(permission_needed):
                return HttpResponseForbidden(f"Access Denied: You don't have {permission_needed} permission")
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator

@login_required
@has_permission(Teacher.CAN_VIEW_ATTENDANCE)
def view_attendance(request, student_id=None):
    """View student attendance (RBAC protected)"""
    context = {
        'student_id': student_id,
        'can_edit': request.user.teacher_profile.has_permission(Teacher.CAN_EDIT_ATTENDANCE),
        'module': 'Attendance'
    }
    return render(request, 'teachers/attendance.html', context)

@login_required
@has_permission(Teacher.CAN_VIEW_MARKS)
def view_marks(request, student_id=None):
    """View student marks (RBAC protected)"""
    context = {
        'student_id': student_id,
        'can_edit': request.user.teacher_profile.has_permission(Teacher.CAN_EDIT_MARKS),
        'module': 'Marks'
    }
    return render(request, 'teachers/marks.html', context)

@login_required
@has_permission(Teacher.CAN_VIEW_FEES)
def view_fees(request, student_id=None):
    """View student fees (RBAC protected)"""
    context = {
        'student_id': student_id,
        'can_edit': request.user.teacher_profile.has_permission(Teacher.CAN_EDIT_FEES),
        'module': 'Fees'
    }
    return render(request, 'teachers/fees.html', context)

@login_required
@has_permission(Teacher.CAN_MANAGE_STUDENTS)
def manage_students(request):
    """Manage students (RBAC protected)"""
    return render(request, 'teachers/manage_students.html')

class TeacherDashboardView(TemplateView):
    template_name = 'teachers/dashboard.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not is_teacher(request.user):
            return HttpResponseForbidden("Access Denied: Teacher only area")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.request.user.teacher_profile
        context['teacher'] = teacher
        context['permissions'] = {
            'can_view_attendance': teacher.has_permission(Teacher.CAN_VIEW_ATTENDANCE),
            'can_edit_attendance': teacher.has_permission(Teacher.CAN_EDIT_ATTENDANCE),
            'can_view_marks': teacher.has_permission(Teacher.CAN_VIEW_MARKS),
            'can_edit_marks': teacher.has_permission(Teacher.CAN_EDIT_MARKS),
            'can_view_fees': teacher.has_permission(Teacher.CAN_VIEW_FEES),
            'can_edit_fees': teacher.has_permission(Teacher.CAN_EDIT_FEES),
            'can_manage_students': teacher.has_permission(Teacher.CAN_MANAGE_STUDENTS),
        }
        return context
