from .models import Attendance
from .serializers import AttendanceSerializer
from users.permissions import IsTeacher,IsAdmin,IsStudent
import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from students.models import Student
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.filters import SearchFilter

logger = logging.getLogger('attendance')


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['date','status']
   
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated, IsAdmin | IsTeacher]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsStudent | IsTeacher | IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Attendance.objects.all()

        user = self.request.user
        if user.role == 'student':
            student = Student.objects.get(user=user)
            return Attendance.objects.filter(student=student)
        elif user.role == 'teacher':
            return Attendance.objects.filter(course__instructor=user)
        return Attendance.objects.all()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        attendance = serializer.instance
        logger.info(
            f"{self.request.user.email} put attendance {attendance.student.user.email} for {attendance.course.name} on {attendance.date} with {attendance.status}")

    def perform_update(self, serializer):
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

    @method_decorator(cache_page(60 * 2, key_prefix='att_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 2, key_prefix='att_detal'))

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)