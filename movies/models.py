from django.db import models
from utils.models import BaseModel

class Movie(BaseModel ):
    title = models.CharField(max_length=255)
    external_id = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)
    rated = models.CharField(max_length=20, blank=True, null=True)
    runtime = models.CharField(max_length=50, blank=True, null=True)
    runtime = models.CharField(max_length=50, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    poster = models.URLField(blank=True, null=True)
    imdb_rating = models.CharField(max_length=10, blank=True, null=True)
    
    
    class Meta:
        ordering = ['title']
        
        def __str__(self):
            return self.title