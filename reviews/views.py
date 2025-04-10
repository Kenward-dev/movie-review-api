from rest_framework import generics, filters, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from .models import Review
from .serializers import ReviewSerializer
from utils.permissions import IsOwnerOrReadOnly
from movies.models import Movie
from utils.pagination import StandardResultsSetPagination
from utils.movie_api import get_or_create_movie, search_external_movies

class ReviewListCreateAPIView(mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                generics.GenericAPIView):
    """
    API view for listing and creating reviews
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['movie__title', 'content']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Review.objects.all()
        
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            try:
                min_rating = int(min_rating)
                queryset = queryset.filter(rating__gte=min_rating)
            except ValueError:
                pass
        
        movie_title = self.request.query_params.get('movie_title')
        if movie_title:
            queryset = queryset.filter(movie__title__icontains=movie_title)
            
        return queryset
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        movie_title = request.data.get('movie_title')
        if movie_title:
            movie = get_or_create_movie(movie_title)
            if not movie:
                external_results = search_external_movies(movie_title)
                if external_results:
                    return Response({
                        "movie_title": f"Found movie '{movie_title}' but couldn't add it to our database. Please try again or contact support."
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        "movie_title": f"Could not find any movie matching '{movie_title}'. Please check spelling or try another title."
                    }, status=status.HTTP_400_BAD_REQUEST)
        
        return self.create(request, *args, **kwargs)


class ReviewDetailAPIView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):
    """
    API view for retrieving, updating, and deleting a review
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        movie_title = request.data.get('movie_title')
        if movie_title:
            movie = get_or_create_movie(movie_title)
            if not movie:
                return Response({
                    "movie_title": f"Could not find movie '{movie_title}'. Please check the title."
                }, status=status.HTTP_400_BAD_REQUEST)
                
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        movie_title = request.data.get('movie_title')
        if movie_title:
            movie = get_or_create_movie(movie_title)
            if not movie:
                return Response({
                    "movie_title": f"Could not find movie '{movie_title}'. Please check the title."
                }, status=status.HTTP_400_BAD_REQUEST)
                
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MovieReviewsAPIView(generics.GenericAPIView):
    """
    API view for getting reviews for a specific movie
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        movie_title = self.request.query_params.get('title', None)
        if not movie_title:
            return Review.objects.none()
        
        movie = Movie.objects.filter(title__icontains=movie_title).first()
        if not movie:
            movie = get_or_create_movie(movie_title)
            
        if not movie:
            return Review.objects.none()
            
        return Review.objects.filter(movie=movie)
    
    def get(self, request, *args, **kwargs):
        movie_title = request.query_params.get('title', None)
        if not movie_title:
            return Response(
                {"detail": "Movie title parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        movie = Movie.objects.filter(title__icontains=movie_title).first()
        if not movie:
            movie = get_or_create_movie(movie_title)
            
        if not movie:
            return Response(
                {"detail": f"Movie '{movie_title}' not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        queryset = Review.objects.filter(movie=movie)
        
        avg_rating = queryset.aggregate(Avg('rating'))
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = {
                'movie': movie.title,
                'average_rating': avg_rating['rating__avg'] or 0,  
                'reviews': serializer.data
            }
            return self.get_paginated_response(response_data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'movie': movie.title,
            'average_rating': avg_rating['rating__avg'] or 0,  
            'reviews': serializer.data
        })