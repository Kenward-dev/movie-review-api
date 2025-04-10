from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from movies.models import Movie
from reviews.models import Review

class ReviewAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            year='2023',
            genre='Drama',
            director='Test Director',
            plot='Test plot description',
            imdb_rating='8.0'
        )
        self.review = Review.objects.create(
            movie=self.movie,
            user=self.user,
            content='Great movie!',
            rating=5
        )
        self.client.force_authenticate(user=self.user)
        self.review_list_url = reverse('review-list')
        self.review_detail_url = reverse('review-detail', args=[self.review.id])

    def test_get_reviews(self):
        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_review(self):
        new_movie = Movie.objects.create(
            title='Another Test Movie',
            year='2022',
            genre='Action',
            director='Another Director',
            plot='Another plot description',
            imdb_rating='7.5'
        )
        
        data = {
            'movie_title': 'Another Test Movie',
            'content': 'Fantastic movie!',
            'rating': 4
        }
        
        response = self.client.post(self.review_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Fantastic movie!')
        self.assertEqual(response.data['rating'], 4)