from django.urls import path
from .views import MovieListAPIView, MovieDetailAPIView, MovieSearchAPIView

urlpatterns = [
    path('', MovieListAPIView.as_view(), name='movie-list'),
    path('<int:pk>/', MovieDetailAPIView.as_view(), name='movie-detail'),
    path('search/', MovieSearchAPIView.as_view(), name='movie-search'),
]