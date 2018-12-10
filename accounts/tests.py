from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class RegistrationTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_signup_incorrect(self):
        data = {
            'email': 'abc',
            'password': 'passwordasdasdasdsa'
        }
        response = self.client.post(reverse('api:accounts:signup'), data=data)
        self.assertEqual(response.status_code, 400)
        data = {
            'email': 'abc@gmail.com',
            'password': ''
        }
        response = self.client.post(reverse('api:accounts:signup'), data=data)
        self.assertEqual(response.status_code, 400)
        data = {}
        response = self.client.post(reverse('api:accounts:signup'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_signup_correct(self):
        data = {
            'email': 'correct@mail.com',
            'password': 'correctpassword'
        }
        response = self.client.post(reverse('api:accounts:signup'), data=data)
        self.assertEqual(response.status_code, 201)
        response = self.client.post(reverse('api:accounts:auth'), data=data)
        self.assertTrue('token' in response.data)
