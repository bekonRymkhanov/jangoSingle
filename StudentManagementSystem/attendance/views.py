from rest_framework import generics, permissions
from .models import Attendance
from .serializers import AttendanceSerializer
from users.permissions import IsTeacher

class AttendanceView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]