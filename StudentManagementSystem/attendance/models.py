from django.db import models
from students.models import Student
from courses.models import Course

class Attendance(models.Model):
    student = models.ForeignKey(
        Student,
        related_name="attendance_records",
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('present', 'Present'), ('absent', 'Absent')])
