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
    
    def create(self, validated_data):
        student_data = validated_data.pop('student')
        course_data = validated_data.pop('course')
        student = Student.objects.get(user__email=student_data['user']['email'])
        course = Course.objects.get(name=course_data['name'])
        attendance = Attendance.objects.create(student=student, course=course, **validated_data)
        return attendance