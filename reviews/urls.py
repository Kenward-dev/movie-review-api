from django.urls import path
from .views import ReviewListCreateAPIView, ReviewDetailAPIView, MovieReviewsAPIView

urlpatterns = [
    path('', ReviewListCreateAPIView.as_view(), name='review-list'),
    path('<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
    path('by-movie/', MovieReviewsAPIView.as_view(), name='movie-reviews'),
]