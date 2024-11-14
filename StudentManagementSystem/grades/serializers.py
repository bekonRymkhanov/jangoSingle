from rest_framework import serializers
from .models import Grade
from students.models import Student
from courses.models import Course

class GradeSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Grade
        fields = ['id', 'student', 'course', 'grade', 'date']
