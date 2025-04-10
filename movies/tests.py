from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from movies.models import Movie

class MovieAPITest(TestCase):
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
        self.client.force_authenticate(user=self.user)
        self.movie_list_url = reverse('movie-list')
        self.movie_detail_url = reverse('movie-detail', args=[self.movie.id])

    def test_get_movies(self):
        response = self.client.get(self.movie_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_get_movie_detail(self):
        response = self.client.get(self.movie_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Movie')