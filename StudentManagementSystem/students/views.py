from rest_framework import generics,permissions
from .models import Student
from .serializers import StudentSerializer
from users.permissions import IsAdmin, IsStudent

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdmin]



class StudentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.IsAuthenticated, IsStudent | IsAdmin]
        elif self.request.method == 'PUT':
            self.permission_classes = [permissions.IsAuthenticated, IsStudent]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Student.objects.filter(user=user)
        return super().get_queryset()
