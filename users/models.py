from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from utils.models import BaseModel


class UserManager(BaseUserManager):
    """
    Define a model manager for the User model with no username filed
    """
    
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("You did not provide a valid email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email, password, **extra_fields)
    
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be a staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be a superuser')
        return self._create_user(email, password, **extra_fields)
    
    
class User(AbstractUser, BaseModel):
    """
    Custom User mdel that uses email as the unique identifier instead of username.
    """
    username = None
    email = models.EmailField('email address', unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
