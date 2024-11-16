from rest_framework import generics, permissions
from .models import Grade
from .serializers import GradeSerializer
from users.permissions import IsTeacher, IsAdmin,IsStudent
import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from students.models import Student
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.filters import SearchFilter

logger = logging.getLogger('grades')



class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['grade','date']
   


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
        user = self.request.user
        if user.role == 'student':
            student = Student.objects.get(user=user)
            return Grade.objects.filter(student=student)
        elif user.role == 'teacher':
            return Grade.objects.filter(teacher=user)
        return Grade.objects.all()


    @method_decorator(cache_page(60 * 2, key_prefix='grade_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 2, key_prefix='grade_detail'))
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

    def perform_create(self, serializer):
        super().perform_create(serializer)
        grade = serializer.instance
        logger.info(
            f"{self.request.user.email} put mark {grade.grade} to {grade.student.user.email} for {grade.course.name}")

    def perform_update(self, serializer):
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
