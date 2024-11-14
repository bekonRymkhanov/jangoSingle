from rest_framework import serializers
from .models import Attendance
from students.models import Student
from courses.models import Course

class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'status']