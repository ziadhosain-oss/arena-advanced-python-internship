import pandas as pd
import io
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import modelformset_factory
from .models import Student, Marks, Attendance
from .forms import AttendanceForm

def mark_attendance(request):
    students = Student.objects.all()
    AttendanceFormSet = modelformset_factory(Attendance, form=AttendanceForm, extra=0)
    
    if request.method == 'POST':
        formset = AttendanceFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('dashboard')
    else:
        initial_data = [{'student': s, 'student_name': s.name} for s in students]
        formset = AttendanceFormSet(queryset=Attendance.objects.none(), initial=initial_data)
    
    return render(request, 'students/mark_attendance.html', {'formset': formset})

def student_dashboard(request):
    query = request.GET.get('search', '')
    students = Student.objects.all().values('id', 'name', 'roll_number')
    marks = Marks.objects.all().values('student_id', 'score')
    attendance = Attendance.objects.all().values('student_id', 'is_present')
    
    # Check if we have data to avoid KeyError
    if not marks.exists() or not students.exists():
        return render(request, 'students/dashboard.html', {
            'error': 'No data available. Please add Students and Marks in Admin.',
            'top_3': [],
            'full_report': []
        })

    df_students = pd.DataFrame(list(students))
    df_marks = pd.DataFrame(list(marks))
    df_attendance = pd.DataFrame(list(attendance))

    avg_marks = df_marks.groupby('student_id')['score'].mean().reset_index()
    attendance_rate = df_attendance.groupby('student_id')['is_present'].mean().reset_index()
    attendance_rate['attendance_percentage'] = attendance_rate['is_present'] * 100

    report_df = pd.merge(df_students, avg_marks, left_on='id', right_on='student_id', how='left')
    report_df = pd.merge(report_df, attendance_rate[['student_id', 'attendance_percentage']], left_on='id', right_on='student_id', how='left')
    report_df = report_df.rename(columns={'score': 'average_score'})
    report_df['average_score'] = report_df['average_score'].fillna(0)
    report_df['attendance_percentage'] = report_df['attendance_percentage'].fillna(0)

    if query:
        report_df = report_df[report_df['name'].str.contains(query, case=False)]

    top_3 = report_df.nlargest(3, 'average_score').to_dict('records')
    full_report = report_df.to_dict('records')

    return render(request, 'students/dashboard.html', {
        'top_3': top_3,
        'full_report': full_report,
        'query': query
    })

def export_performance_excel(request):
    students = Student.objects.all().values('id', 'name', 'roll_number')
    marks = Marks.objects.all().values('student_id', 'score')
    attendance = Attendance.objects.all().values('student_id', 'is_present')
    
    # Prevention: If no marks exist, don't run Pandas groupby
    if not marks.exists():
        return HttpResponse("No data available to export. Please add marks first.", content_type="text/plain")

    df_students = pd.DataFrame(list(students))
    df_marks = pd.DataFrame(list(marks))
    df_attendance = pd.DataFrame(list(attendance))
    
    avg_marks = df_marks.groupby('student_id')['score'].mean().reset_index()
    attendance_rate = df_attendance.groupby('student_id')['is_present'].mean().reset_index()
    attendance_rate['Attendance Percentage'] = attendance_rate['is_present'] * 100

    report_df = pd.merge(df_students, avg_marks, left_on='id', right_on='student_id', how='left')
    report_df = pd.merge(report_df, attendance_rate[['student_id', 'Attendance Percentage']], left_on='id', right_on='student_id', how='left')
    report_df = report_df.rename(columns={'score': 'Average Score'})
    report_df['Average Score'] = report_df['Average Score'].fillna(0)
    report_df['Attendance Percentage'] = report_df['Attendance Percentage'].fillna(0)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        report_df.to_excel(writer, index=False, sheet_name='Performance')
    
    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=student_report.xlsx'
    return response

def export_performance_csv(request):
    students = Student.objects.all().values('id', 'name', 'roll_number')
    marks = Marks.objects.all().values('student_id', 'score')
    attendance = Attendance.objects.all().values('student_id', 'is_present')
    
    # Prevention: If no marks exist, don't run Pandas groupby
    if not marks.exists():
        return HttpResponse("No data available to export. Please add marks first.", content_type="text/plain")

    df_students = pd.DataFrame(list(students))
    df_marks = pd.DataFrame(list(marks))
    df_attendance = pd.DataFrame(list(attendance))
    
    avg_marks = df_marks.groupby('student_id')['score'].mean().reset_index()
    attendance_rate = df_attendance.groupby('student_id')['is_present'].mean().reset_index()
    attendance_rate['Attendance Percentage'] = attendance_rate['is_present'] * 100

    report_df = pd.merge(df_students, avg_marks, left_on='id', right_on='student_id', how='left')
    report_df = pd.merge(report_df, attendance_rate[['student_id', 'Attendance Percentage']], left_on='id', right_on='student_id', how='left')
    report_df = report_df.rename(columns={'score': 'Average Score'})
    report_df['Average Score'] = report_df['Average Score'].fillna(0)
    report_df['Attendance Percentage'] = report_df['Attendance Percentage'].fillna(0)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=student_report.csv'
    report_df.to_csv(response, index=False)
    return response