from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer
import logging
from .exeptions import ItemNotFoundException  # custom exception handler

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.filters import SearchFilter


logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict to authenticated users
    filter_backends = [SearchFilter]
    search_fields = ['email','role']
   



    def perform_create(self, serializer):
        super().perform_create(serializer)

    @method_decorator(cache_page(60*2))
    def list(self, request, *args, **kwargs):
        logger.debug("Listing items")
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except User.DoesNotExist:
            raise ItemNotFoundException()
        
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)