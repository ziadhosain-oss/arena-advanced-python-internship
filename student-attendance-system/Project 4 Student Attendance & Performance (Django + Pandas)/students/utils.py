import pandas as pd
from .models import Student, Attendance, Marks

def get_performance_report():
    # Convert Students to DataFrame
    students = Student.objects.all().values('id', 'name', 'roll_number')
    df_students = pd.DataFrame(list(students))

    if df_students.empty:
        return None

    # Calculate Attendance %
    attendance = Attendance.objects.all().values('student_id', 'is_present')
    if attendance:
        df_att = pd.DataFrame(list(attendance))
        # Group by student and find the mean of 'is_present' (True=1, False=0)
        att_stats = df_att.groupby('student_id')['is_present'].mean() * 100
        df_students['attendance_pct'] = df_students['id'].map(att_stats).fillna(0)
    else:
        df_students['attendance_pct'] = 0

    # Calculate Average Marks
    marks = Marks.objects.all().values('student_id', 'score')
    if marks:
        df_marks = pd.DataFrame(list(marks))
        avg_marks = df_marks.groupby('student_id')['score'].mean()
        df_students['avg_marks'] = df_students['id'].map(avg_marks).fillna(0)
    else:
        df_students['avg_marks'] = 0

    return df_students