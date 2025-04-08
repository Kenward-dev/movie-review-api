from django.urls import path
from .views import GoogleAuthView, EmailPasswordLoginView, CurrentUserView

urlpatterns = [
    path('google/', GoogleAuthView.as_view(), name='google-auth'),
    path('login/', EmailPasswordLoginView.as_view(), name='email-password-login'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
]