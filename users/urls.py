from django.urls import path
from .views import UserListCreate, UserRetrieveUpdateDestroy

urlpatterns = [
    path('', UserListCreate.as_view(), name='user-list-create'),
    path('<uuid:pk>/', UserRetrieveUpdateDestroy.as_view(), name='user-detail')
]
