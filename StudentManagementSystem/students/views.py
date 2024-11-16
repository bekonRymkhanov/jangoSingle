from rest_framework import generics,permissions
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsAdmin, IsStudent
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import logging
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.filters import SearchFilter


logger = logging.getLogger('students')


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['registration_date','name','dob','student_id']
   



    def get_permissions(self):
        if self.action in ['retrieve', 'update']:
            permission_classes = [IsAuthenticated, IsStudent | IsAdmin]
        elif self.action in ['list', 'create']:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Student.objects.filter(user=user)
        return Student.objects.select_related()
        
    @method_decorator(cache_page(60 * 2, key_prefix='student_list'))
    def list(self, request, *args, **kwargs):
        logger.info(
            f"{self.request.user.email} listed students")

        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 2, key_prefix='student_detail'))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        super().perform_update(serializer)
        student = serializer.instance
        logger.info(f"Студент {student.user.email} обновил свой профиль")

