from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from unittest.mock import patch
from customer.models.models import Customer
from orders.models.models import Orders
from orders.serializers.serializers import OrdersSerializer


class OrdersTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            phone_number='+254712345678',
            password='password123'
        )
        self.client.force_authenticate(user=self.customer)

        self.valid_order_data = {
            'customer': self.customer.id,
            'item': 'Laptop',
            'amount': '1200.00'
        }
        self.invalid_order_data = {
            'customer': self.customer.id,
            'item': '',
            'amount': '-10.00'
        }

    def test_create_order_success(self):
        with patch('orders.views.order_viewset.send_sms') as mock_sms:
            mock_sms.return_value = {'status': 'success'}

            response = self.client.post(reverse('order-list'), self.valid_order_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Orders.objects.count(), 1)
            self.assertEqual(Orders.objects.get().item, 'Laptop')
            mock_sms.assert_called_once_with(
                self.customer.phone_number,
                'Dear Test User, your order for Laptop has been placed successfully.'
            )

    def test_create_order_invalid_data(self):
        response = self.client.post(reverse('order-list'), self.invalid_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Orders.objects.count(), 0)

    def test_create_order_requires_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('order-list'), self.valid_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sms_failure_still_creates_order(self):
        with patch('orders.views.order_viewset.send_sms') as mock_sms:
            mock_sms.return_value = None

            response = self.client.post(reverse('order-list'), self.valid_order_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Orders.objects.count(), 1)
            self.assertIn('failed to send SMS', response.data.get('message', ''))

    def test_order_serializer_valid_data(self):
        serializer = OrdersSerializer(data=self.valid_order_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_order_serializer_invalid_amount(self):
        data = {**self.valid_order_data, 'amount': '-10.00'}
        serializer = OrdersSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('amount', serializer.errors)

    def test_order_serializer_invalid_item(self):
        data = {**self.valid_order_data, 'item': 'ab'}
        serializer = OrdersSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('item', serializer.errors)

    def test_list_customer_orders(self):
        Orders.objects.create(customer=self.customer, item='Phone', amount='500.00')

        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['item'], 'Phone')
        self.assertEqual(str(response.json()[0]['amount']), '500.00')

    def test_list_orders_only_returns_own_orders(self):
        other_customer = Customer.objects.create_user(
            email='other@example.com',
            name='Other User',
            phone_number='+254711111111',
            password='password123'
        )
        Orders.objects.create(customer=self.customer, item='Phone', amount='500.00')
        Orders.objects.create(customer=other_customer, item='TV', amount='900.00')

        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['item'], 'Phone')
