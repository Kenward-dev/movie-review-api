from rest_framework import generics, filters, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie
from .serializers import MovieSerializer
from utils.pagination import StandardResultsSetPagination
from utils.movie_api import search_external_movies

class MovieListAPIView(mixins.ListModelMixin,
                        generics.GenericAPIView):
    """
    API view for listing and searching movies
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'genre', 'director', 'actors']
    ordering_fields = ['title', 'year', 'imdb_rating']
    ordering = ['title']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
            
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(year=year)
            
        return queryset
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MovieDetailAPIView(mixins.RetrieveModelMixin,
                            generics.GenericAPIView):
    """
    API view for retrieving a specific movie
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class MovieSearchAPIView(generics.GenericAPIView):
    """
    API view for advanced movie searching (local + external)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MovieSerializer
    
    def get(self, request, *args, **kwargs):
        search_term = request.query_params.get('q', '')
        
        if not search_term or len(search_term) < 2:
            return Response(
                {"detail": "Search term must be at least 3 characters"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        local_movies = Movie.objects.filter(title__icontains=search_term)[:5]
        local_results = self.get_serializer(local_movies, many=True).data
        
        external_results = search_external_movies(search_term)
        
        return Response({
            'local_results': local_results,
            'external_results': external_results
        })