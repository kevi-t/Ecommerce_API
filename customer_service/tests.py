from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Customer
from django.contrib.auth import get_user_model

# Test for the Customer model and registration API
class CustomerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_customer_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'phone_number': '1234567890',
            'password': 'testpassword123'
        }
        self.invalid_customer_data = {
            'name': '',
            'email': 'invalid-email',
            'phone_number': '1234567890',
            'password': 'short'
        }

    def test_create_customer_model(self):
        """Test customer creation in the model directly"""
        customer = Customer.objects.create_user(
            email=self.valid_customer_data['email'],
            name=self.valid_customer_data['name'],
            phone_number=self.valid_customer_data['phone_number'],
            password=self.valid_customer_data['password']
        )
        self.assertEqual(customer.email, self.valid_customer_data['email'])
        self.assertTrue(customer.check_password(self.valid_customer_data['password']))

    def test_create_superuser_model(self):
        """Test superuser creation"""
        superuser = Customer.objects.create_superuser(
            email="admin@example.com",
            name="Admin User",
            phone_number="0987654321",
            password="adminpassword"
        )
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.has_perm('test_perm'))

    def test_register_customer_success(self):
        """Test API to register a valid customer"""
        response = self.client.post(reverse('register_user'), self.valid_customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Customer registered successfully!')
        # Verify customer is created in the database
        customer = Customer.objects.get(email=self.valid_customer_data['email'])
        self.assertIsNotNone(customer)

    def test_register_customer_invalid(self):
        """Test API to register an invalid customer"""
        response = self.client.post(reverse('register_user'), self.invalid_customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)

    def test_test_endpoint(self):
        """Test the simple test view"""
        response = self.client.get(reverse('test'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"Message": "Application test successful"})

    def test_password_validation(self):
        """Test password validation on customer creation"""
        invalid_password_data = {
            'name': 'Jane Doe',
            'email': 'janedoe@example.com',
            'phone_number': '0987654321',
            'password': 'short'
        }
        response = self.client.post(reverse('register_user'), invalid_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
