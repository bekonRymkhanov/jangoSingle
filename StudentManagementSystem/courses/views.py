from rest_framework import generics, permissions
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from users.permissions import IsTeacher, IsAdmin,IsStudent
import logging
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page





logger = logging.getLogger('courses')


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @method_decorator(cache_page(60 * 2, key_prefix='course_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 2, key_prefix='course_detail'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        super().perform_create(serializer)
        logger.info(f'{serializer.instance.student} enrolled {serializer.instance.course}')

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        logger.info(f'{instance.student} de enrolled {instance.course}')

    @method_decorator(cache_page(60 * 2, key_prefix='enrollment_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)