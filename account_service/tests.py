from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APIClient
from account_service.custom_auth_backend import EmailBackend

Customer = get_user_model()

class AuthViewsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user = Customer.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            name='Test User',
            phone_number='123456789'
        )
        self.client = APIClient()

    def test_login_user_success(self):
        response = self.client.post(reverse('login_user'), {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_user_invalid_credentials(self):
        response = self.client.post(reverse('login_user'), {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    @patch('requests.post')
    @patch('requests.get')
    def test_oidc_callback_success(self, mock_get, mock_post):
        # Mock the token and user info responses
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'access_token': 'fake_access_token'
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'email': 'testuser@example.com',
            'name': 'Test User',
            'phone_number': '123456789'
        }

        response = self.client.get(reverse('oidc_callback'), {'code': 'fake_code'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect to success page

    @patch('requests.post')
    def test_oidc_callback_invalid_code(self, mock_post):
        # Mock an invalid token response
        mock_post.return_value.status_code = 400
        response = self.client.get(reverse('oidc_callback'), {'code': 'invalid_code'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Failed to fetch token')

    def test_success_view(self):
        response = self.client.get(reverse('success'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Authentication was successful!")

    def test_oidc_login_redirect(self):
        response = self.client.get(reverse('oidc_login'))
        self.assertEqual(response.status_code, 302)  # Should redirect to OIDC provider


class EmailBackendTest(TestCase):
    def setUp(self):
        self.user = Customer.objects.create_user(
            email='backenduser@example.com',
            password='backendpassword',
            name='Backend User',
            phone_number='987654321'
        )

    def test_authenticate_with_valid_credentials(self):
        backend = EmailBackend()
        user = backend.authenticate(request=None, email='backenduser@example.com', password='backendpassword')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'backenduser@example.com')

    def test_authenticate_with_invalid_credentials(self):
        backend = EmailBackend()
        user = backend.authenticate(request=None, email='backenduser@example.com', password='wrongpassword')
        self.assertIsNone(user)

    def test_get_user(self):
        backend = EmailBackend()
        user = backend.get_user(self.user.id)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'backenduser@example.com')

    def test_get_nonexistent_user(self):
        backend = EmailBackend()
        user = backend.get_user(999)  # ID that doesn't exist
        self.assertIsNone(user)
