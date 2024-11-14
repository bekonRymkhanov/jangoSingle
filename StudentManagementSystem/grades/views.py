from rest_framework import generics, permissions
from .models import Grade
from .serializers import GradeSerializer
from users.permissions import IsTeacher, IsAdmin

class GradeListCreateView(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher | IsAdmin]
