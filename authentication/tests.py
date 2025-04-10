from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User

class EmailPasswordAuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        self.login_url = reverse('email-password-login')
        self.current_user_url = reverse('current-user')

    def test_user_login(self):
        response = self.client.post(
            self.login_url,
            {'email': 'test@example.com', 'password': 'testpassword123'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_current_user_authenticated(self):
        # Login first
        login_response = self.client.post(
            self.login_url,
            {'email': 'test@example.com', 'password': 'testpassword123'},
            format='json'
        )
        token = login_response.data['access']
        
        # Use token to access protected endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.current_user_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')