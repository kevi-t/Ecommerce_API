from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from unittest.mock import patch
from customer.models.models import Customer
from customer.authentication.custom_auth_backend import EmailBackend


class CustomerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_customer_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone_number': '0722123456',
            'password': 'testpassword123'
        }

    def test_create_customer_model(self):
        customer = Customer.objects.create_user(
            email='johndoe@example.com',
            name='John Doe',
            phone_number='+254722123456',
            password='testpassword123'
        )
        self.assertEqual(customer.email, 'johndoe@example.com')
        self.assertTrue(customer.check_password('testpassword123'))

    def test_create_superuser_model(self):
        superuser = Customer.objects.create_superuser(
            email='admin@example.com',
            name='Admin User',
            phone_number='+254798765432',
            password='adminpassword'
        )
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.has_perm('test_perm'))

    def test_register_customer_success(self):
        response = self.client.post(reverse('customer-list'), self.valid_customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Customer registered successfully!')
        self.assertIsNotNone(Customer.objects.get(email='johndoe@example.com'))

    def test_register_customer_duplicate_email(self):
        self.client.post(reverse('customer-list'), self.valid_customer_data, format='json')
        response = self.client.post(reverse('customer-list'), self.valid_customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_customer_invalid_email(self):
        data = {**self.valid_customer_data, 'email': 'not-an-email'}
        response = self.client.post(reverse('customer-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        data = {**self.valid_customer_data, 'password': 'short'}
        response = self.client.post(reverse('customer-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = Customer.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            name='Test User',
            phone_number='+254712345678'
        )

    def test_login_success(self):
        response = self.client.post(reverse('customer-login'), {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('customer-login'), {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    def test_get_profile_requires_auth(self):
        response = self.client.get(reverse('customer-profile'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_success(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(reverse('customer-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')

    def test_update_profile_success(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.patch(reverse('customer-profile'), {'name': 'Updated Name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Profile updated successfully.')

    @patch('requests.post')
    @patch('requests.get')
    def test_oidc_callback_success(self, mock_get, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'access_token': 'fake_access_token'}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'email': 'testuser@example.com',
            'name': 'Test User',
            'phone_number': '+254712345678'
        }
        response = self.client.get(reverse('oidc_callback'), {'code': 'fake_code'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('requests.post')
    def test_oidc_callback_missing_code(self, mock_post):
        response = self.client.get(reverse('oidc_callback'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_oidc_login_redirects(self):
        response = self.client.get(reverse('oidc_login'))
        self.assertEqual(response.status_code, 302)


class EmailBackendTest(TestCase):
    def setUp(self):
        self.user = Customer.objects.create_user(
            email='backenduser@example.com',
            password='backendpassword',
            name='Backend User',
            phone_number='+254787654321'
        )

    def test_authenticate_valid_credentials(self):
        backend = EmailBackend()
        user = backend.authenticate(request=None, email='backenduser@example.com', password='backendpassword')
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'backenduser@example.com')

    def test_authenticate_invalid_credentials(self):
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
        self.assertIsNone(backend.get_user(99999))
