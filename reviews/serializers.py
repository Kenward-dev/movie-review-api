from rest_framework import serializers
from .models import Review
from users.serializers import UserSerializer
from movies.serializers import MovieSerializer
from utils.movie_api import get_or_create_movie

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    movie_title = serializers.CharField(write_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'movie', 'movie_title', 'content', 'rating',
            'user', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'movie']
    
    def validate(self, data):
        if 'rating' in data and (data['rating'] < 1 or data['rating'] > 5):
            raise serializers.ValidationError({"rating": "Rating must be between 1 and 5"})
        
        if self.instance is None:  
            if not data.get('movie_title'):
                raise serializers.ValidationError({"movie_title": "Movie title is required"})
            if not data.get('content'):
                raise serializers.ValidationError({"content": "Review content is required"})
            
            movie_title = data.get('movie_title')
            if movie_title:
                movie = get_or_create_movie(movie_title)
                if not movie:
                    raise serializers.ValidationError({
                        "movie_title": f"Movie '{movie_title}' could not be found. Please check the title or try a different movie."
                    })
        
        return data
    
    def create(self, validated_data):
        # Get movie title and fetch/create movie
        movie_title = validated_data.pop('movie_title')
        movie = get_or_create_movie(movie_title)
        
        # CORRECTION: Better error message
        if not movie:
            raise serializers.ValidationError({
                "movie_title": f"Movie '{movie_title}' could not be found or created. Please try a different title."
            })
        
        # Create the review with the movie
        validated_data['movie'] = movie
        validated_data['user'] = self.context['request'].user
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'movie_title' in validated_data:
            movie_title = validated_data.pop('movie_title')
            movie = get_or_create_movie(movie_title)
            
            if not movie:
                raise serializers.ValidationError({
                    "movie_title": f"Movie '{movie_title}' could not be found or created. Please try a different title."
                })
            
            instance.movie = movie
        
        return super().update(instance, validated_data)