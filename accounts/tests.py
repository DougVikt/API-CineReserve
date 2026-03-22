from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User


class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')

    def test_register_success(self):
        data = {
            'username': 'testuser',
            'email': 'test@email.com',
            'password': 'senha123@',
            'password_check': 'senha123@',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_password_mismatch(self):
        data = {
            'username': 'testuser',
            'email': 'test@email.com',
            'password': 'senha123@',
            'password_check': 'senha456@',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        User.objects.create_user(username='testuser', password='senha123@')
        data = {
            'username': 'testuser',
            'email': 'test@email.com',
            'password': 'senha123@',
            'password_check': 'senha123@',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('token_obtain_pair')
        User.objects.create_user(username='testuser', password='senha123@')

    def test_login_success(self):
        data = {
            'username': 'testuser',
            'password': 'senha123@',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        data = {
            'username': 'testuser',
            'password': 'senhaerrada',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)