from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Category, Transaction

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('auth_register')
        self.token_url = reverse('token_obtain_pair')

    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertNotIn('password', response.data)

    def test_token_obtain(self):
        User.objects.create_user(username='testuser', password='testpassword123')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class FinanceTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pw1')
        self.user2 = User.objects.create_user(username='user2', password='pw2')
        self.client.force_authenticate(user=self.user1)

    def test_category_crud(self):
        # Create
        res = self.client.post('/api/categories/', {'name': 'Food', 'type': 'EXPENSE'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        cat_id = res.data['id']

        # List
        res = self.client.get('/api/categories/')
        self.assertEqual(len(res.data), 1)

        # Ensure isolation
        client2 = APIClient()
        client2.force_authenticate(user=self.user2)
        res2 = client2.get('/api/categories/')
        self.assertEqual(len(res2.data), 0)

        # Delete
        res = self.client.delete(f'/api/categories/{cat_id}/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_transaction_crud(self):
        cat = Category.objects.create(user=self.user1, name='Salary', type='INCOME')
        
        # Create
        data = {'amount': '100.00', 'date': '2026-07-01', 'category': cat.id}
        res = self.client.post('/api/transactions/', data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        txn_id = res.data['id']

        # List and Paginate
        res = self.client.get('/api/transactions/?limit=10')
        self.assertIn('results', res.data)
        self.assertEqual(len(res.data['results']), 1)

        # Filter by date
        res = self.client.get('/api/transactions/?limit=10&start_date=2026-07-02')
        self.assertEqual(len(res.data['results']), 0)
        
        # Delete
        res = self.client.delete(f'/api/transactions/{txn_id}/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
