from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.FloatField()

    # This inner class fixes the spelling in Admin
    class Meta:
        verbose_name = "Marks"
        verbose_name_plural = "Marks"

    def __str__(self):
        return f"{self.student.name} - {self.subject}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {self.date}"