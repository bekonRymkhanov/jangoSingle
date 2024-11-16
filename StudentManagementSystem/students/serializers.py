from rest_framework import serializers
from .models import Student
from users.serializers import UserSerializer
from users.models import User
from django.core.cache import cache



class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(),  
        write_only=True,
        required=False  # Make it optional here
    )
    user = serializers.StringRelatedField(read_only=True)
    enrollments = serializers.SerializerMethodField()
    grades = serializers.SerializerMethodField()
    attendance_records = serializers.SerializerMethodField()
    student_id = serializers.IntegerField()
    name = serializers.CharField()
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'user_id','name','student_id', 'dob', 'registration_date', 'enrollments', 'grades', 'attendance_records']


    def get_enrollments(self, obj):
        enrollments = obj.enrollments.all()  # Uses the related_name 'enrollments'
        return [
            {
                'id': enrollment.id,
                'course_id': enrollment.course.id,
                'course_name': enrollment.course.name,
                'enrolled_at': enrollment.enrolled_at
            }
            for enrollment in enrollments
        ]

    def get_grades(self, obj):
        grades = obj.grades.all()
        return [
            {
                'id': grade.id,
                'course_id': grade.course.id,
                'course_name': grade.course.name,
                'grade': grade.grade,
                'date': grade.date
            }
            for grade in grades
        ]

    def get_attendance_records(self, obj):
        attendance_records = obj.attendance_records.all()
        return [
            {
                'id': attendance.id,
                'course_id': attendance.course.id,
                'course_name': attendance.course.name,
                'date': attendance.date,
                'status': attendance.status
            }
            for attendance in attendance_records
        ]

    def create(self, validated_data):
        user = validated_data.pop('user_id')  # Extract the user
        student_id = validated_data.get('student_id')  # Ensure student_id is present

        if not student_id:
            raise serializers.ValidationError({"student_id": "This field is required."})

        student = Student.objects.create(user=user, **validated_data)
        return student

    def update(self, instance, validated_data):
        cache_key_detail = f"student_detail_{instance.id}" 
        cache.delete(cache_key_detail)  

        cache.delete('student_list')
        if 'user_id' in validated_data:
            raise serializers.ValidationError({"user_id": "Updating user_id is not allowed."})
       
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

