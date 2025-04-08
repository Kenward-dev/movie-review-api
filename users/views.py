from rest_framework import generics, mixins, permissions
from .models import User
from .serializers import UserSerializer, UserCreationSerializer
from utils.permissions import IsSelfOrReadOnly


class UserListCreate(
    generics.GenericAPIView, 
    mixins.CreateModelMixin, 
    mixins.ListModelMixin):
    """
    API endpoint that creates and views users.
    """
    
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreationSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    
class UserRetrieveUpdateDestroy(
    generics.GenericAPIView, 
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin
):
    """
    API endpoint that allows a user instance to be retrieved, updated and deleted
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsSelfOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserCreationSerializer
        return UserSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
