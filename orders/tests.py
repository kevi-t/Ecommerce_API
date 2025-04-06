# from django.test import TestCase
# from django.urls import reverse

# from rest_framework.test import APIClient
# from rest_framework import status

# from unittest.mock import patch
# from customer.models.models import Customer
# from orders.models.models import Orders
# from .serializers.serializers import OrdersSerializer


# class OrdersServiceTests(TestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.customer = Customer.objects.create_user(
#             email='testuser@example.com',
#             name='Test User',
#             phone_number='+254712345678',  # Ensure the correct phone number format
#             password='password123'
#         )
#         self.client.force_authenticate(user=self.customer)

#         self.valid_order_data = {
#             'customer': self.customer.id,
#             'item': 'Laptop',
#             'amount': '1200.00'
#         }
#         self.invalid_order_data = {
#             'customer': self.customer.id,
#             'item': '',  # Invalid item
#             'amount': '-10.00'  # Invalid amount
#         }

#     def test_create_order_success(self):
#         """Test creating an order successfully"""
#         with patch('orders.services.send_sms') as mock_send_sms:
#             mock_send_sms.return_value = {'status': 'success'}

#             response = self.client.post(reverse('create_order'), self.valid_order_data, format='json')
#             self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#             self.assertEqual(Orders.objects.count(), 1)
#             self.assertEqual(Orders.objects.get().item, 'Laptop')
#             mock_send_sms.assert_called_once_with(
#                 self.customer.phone_number,
#                 'Dear Test User, your order for Laptop has been placed successfully.'
#             )

#     def test_create_order_invalid_data(self):
#         """Test creating an order with invalid data"""
#         response = self.client.post(reverse('create_order'), self.invalid_order_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Orders.objects.count(), 0)

#     def test_sms_failure(self):
#         """Test creating an order where SMS sending fails"""
#         with patch('orders.services.send_sms') as mock_send_sms:
#             mock_send_sms.side_effect = Exception("SMS sending failed")  # Simulate SMS failure

#             response = self.client.post(reverse('create_order'), self.valid_order_data, format='json')
#             self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#             self.assertEqual(Orders.objects.count(), 1)
#             self.assertIn('Order created successfully, but failed to send SMS.', response.data.get('message', ''))

#     def test_order_serializer_validation(self):
#         """Test the validation logic in the OrderSerializer"""
#         # Test valid data
#         serializer = OrdersSerializer(data=self.valid_order_data)
#         self.assertTrue(serializer.is_valid(), serializer.errors)

#         # Test invalid amount
#         invalid_data = self.invalid_order_data.copy()
#         invalid_data['item'] = 'Laptop'
#         serializer = OrdersSerializer(data=invalid_data)
#         self.assertFalse(serializer.is_valid(), serializer.errors)

#         # Test invalid item
#         invalid_data['item'] = ''
#         invalid_data['amount'] = '100.00'
#         serializer = OrdersSerializer(data=invalid_data)
#         self.assertFalse(serializer.is_valid(), serializer.errors)

#     def test_get_customer_orders(self):
#         """Test fetching orders for a customer"""
#         order = Orders.objects.create(customer=self.customer, item="Phone", amount="500.00")

#         response = self.client.get(reverse('customer-orders'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         orders_data = response.json()
#         self.assertEqual(len(orders_data), 1)
#         self.assertEqual(orders_data[0]['item'], 'Phone')
#         self.assertEqual(str(orders_data[0]['amount']), '500.00')