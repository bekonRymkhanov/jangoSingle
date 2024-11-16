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
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    class Meta:
        model = Enrollment
        fields = ['course', 'student']

        
    def create(self, validated_data):
        student_data = validated_data.pop('student') 
        course_data = validated_data.pop('course')
        
        student = Student.objects.get(id=student_data.id)  
        course = Course.objects.get(id=course_data.id) 
        
        enrollment = Enrollment.objects.create(student=student, course=course, **validated_data)
        return enrollment