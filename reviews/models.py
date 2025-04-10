from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from movies.models import Movie
from utils.models import BaseModel

class Review(BaseModel):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    content = models.TextField()
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Rating must be at least 1"),
            MaxValueValidator(5, message="Rating cannot exceed 5")
        ]
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'movie']
    
    def __str__(self):
        return f"{self.movie.title} - {self.rating}/5 by {self.user.email}"