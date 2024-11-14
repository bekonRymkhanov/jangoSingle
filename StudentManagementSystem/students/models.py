from django.db import models
from django.conf import settings

class Student(models.Model):
    name = models.CharField(max_length=255, default="SomeName")
    student_id = models.IntegerField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dob = models.DateField()
    registration_date = models.DateField(auto_now_add=True)