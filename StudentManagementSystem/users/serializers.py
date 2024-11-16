from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(help_text="email")
    username = serializers.CharField(help_text="username.")
    role = serializers.CharField(help_text="'student', 'teacher', 'admin'")

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
