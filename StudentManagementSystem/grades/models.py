from django.db import models
from students.models import Student
from courses.models import Course
from users.models import User

class Grade(models.Model):
    student = models.ForeignKey(
        Student,
        related_name="grades",
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
