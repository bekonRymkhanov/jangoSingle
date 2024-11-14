from rest_framework import serializers
from .models import Course, Enrollment
from students.models import Student

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'instructor']

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    class Meta:
        model = Enrollment
        fields = ['course', 'student']
