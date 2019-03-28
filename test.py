from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from customer.models import Customer

class AccountTests(APITestCase):
    def test_create_customer(self):
        url = reverse('customer-list')
        data = {
            'id': '550e8400-e29b-41d4-a716-446655440000',
            'name': 'John',
            'surname': 'Smith',
            'email': 'jsmith@test.com',
            'phone': '609148275'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().name, 'John')