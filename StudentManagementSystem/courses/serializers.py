from rest_framework import serializers
from .models import Course, Enrollment
from students.models import Student
from users.models import User

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='teacher'))

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'instructor']
    
    def create(self, validated_data):
        return Course.objects.create(**validated_data)


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    class Meta:
        model = Enrollment
        fields = ['course', 'student']

        
    def create(self, validated_data):
        student_data = validated_data.pop('student')
        course_data = validated_data.pop('course')
        student = Student.objects.get(user__email=student_data['user']['email'])
        course = Course.objects.get(name=course_data['name'])
        enrollment = Enrollment.objects.create(student=student, course=course, **validated_data)
        return enrollment