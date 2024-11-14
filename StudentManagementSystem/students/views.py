from rest_framework import generics,permissions
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsAdmin, IsStudent
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import logging
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

logger = logging.getLogger('students')


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


    def get_permissions(self):
        if self.action in ['retrieve', 'update']:
            permission_classes = [IsAuthenticated, IsStudent | IsAdmin]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Student.objects.filter(user=user)
        return Student.objects.all()

    @method_decorator(cache_page(60 * 2, key_prefix='student_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 2, key_prefix='student_detail'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        student = serializer.instance
        logger.info(f"{student.user.email} updatedhis profile")