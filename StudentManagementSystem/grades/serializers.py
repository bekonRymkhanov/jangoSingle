from rest_framework import serializers
from .models import Grade
from students.models import Student
from courses.models import Course
from users.models import User

class GradeSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='teacher'))
    class Meta:
        model = Grade
        fields = ['id', 'student', 'course', 'grade', 'date','teacher']
    def create(self, validated_data):
        return Grade.objects.create(**validated_data)