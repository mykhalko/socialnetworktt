import os

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from socialnetwork.settings import BASE_DIR


def authenticate(c, email, password):
    auth_credentials = {
        'email': email,
        'password': password
    }
    url = reverse('api:accounts:auth')
    response = c.post(url, data=auth_credentials)
    token = response.data['token']
    c.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    return c


class PostAPIViewTestCase(TestCase):

    fixtures = [os.path.join(BASE_DIR, 'fixtures/accounts.json'),
                os.path.join(BASE_DIR, 'fixtures/posts.json')]

    def setUp(self):
        c = APIClient()
        self.c = c

    def test_unauthenticated_get(self):
        response = self.c.get(reverse('api:posts:detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_delete(self):
        response = self.c.delete(reverse('api:posts:detail', args=[1]))
        self.assertEqual(response.status_code, 401)

    def test_authenticated_get(self):
        authenticate(self.c, 'newpublisher@gmail.com', 'publisherpassword')
        response = self.c.get(reverse('api:posts:detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_delete_not_own(self):
        authenticate(self.c, 'newpublisher@gmail.com', 'publisherpassword')
        response = self.c.delete(reverse('api:posts:detail', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_authenticated_delete_own_post(self):
        authenticate(self.c, 'newpublisher@gmail.com', 'publisherpassword')
        response = self.c.delete(reverse('api:posts:detail', args=[9]))
        self.assertEqual(response.status_code, 204)

    def test_authenticated_as_staff_delete_not_own_post(self):
        authenticate(self.c, 'admin@admin.com', 'adminpassword')
        response = self.c.delete(reverse('api:posts:detail', args=[8]))
        self.assertEqual(response.status_code, 204)

    def test_post_like_unlike(self):
        authenticate(self.c, 'newpublisher@gmail.com', 'publisherpassword')
        data = {
            'action': 'like'
        }
        response = self.c.post(reverse('api:posts:detail', args=[9]), data=data)
        self.assertEqual(response.status_code, 200)
        response = self.c.get(reverse('api:posts:detail', args=[9]))
        self.assertEqual(len(response.data['likes']), 1)
        data = {
            'action': 'unlike'
        }
        response = self.c.post(reverse('api:posts:detail', args=[9]), data=data)
        self.assertEqual(response.status_code, 200)
        response = self.c.get(reverse('api:posts:detail', args=[9]))
        self.assertEqual(len(response.data['likes']), 0)

    def test_double_like(self):
        authenticate(self.c, 'newpublisher@gmail.com', 'publisherpassword')
        data = {
            'action': 'like'
        }
        response = self.c.post(reverse('api:posts:detail', args=[9]), data=data)
        self.assertEqual(response.status_code, 200)
        response = self.c.get(reverse('api:posts:detail', args=[9]))
        self.assertEqual(len(response.data['likes']), 1)
        response = self.c.post(reverse('api:posts:detail', args=[9]), data=data)
        self.assertEqual(response.status_code, 200)
        response = self.c.get(reverse('api:posts:detail', args=[9]))
        self.assertEqual(len(response.data['likes']), 1)


class PostListAPIViewTestCase(TestCase):

    fixtures = [os.path.join(BASE_DIR, 'fixtures/accounts.json'),
                os.path.join(BASE_DIR, 'fixtures/posts.json')]

    def setUp(self):
        c = APIClient()
        self.c = c

    def test_unauthenticated_get(self):
        response = self.c.get(reverse('api:posts:list'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_post(self):
        data = {'title': 'abc', 'text': 'ccc'}
        response = self.c.post(reverse('api:posts:list'), data=data)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_list(self):
        authenticate(self.c, 'newpublisher@gmail.com', 'publisherpassword')
        response = self.c.get(reverse('api:posts:list'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_post_correct_data(self):
        data = {'title': 'abc', 'text': 'ccc'}
        authenticate(self.c, 'newpublisher@gmail.com', 'publisherpassword')
        response = self.c.post(reverse('api:posts:list'), data=data)
        self.assertEqual(response.status_code, 201)

    def test_authenticated_post_incorrect_data(self):
        data = {'text': 'ccc'}
        authenticate(self.c, 'newpublisher@gmail.com', 'publisherpassword')
        response = self.c.post(reverse('api:posts:list'), data=data)
        self.assertEqual(response.status_code, 400)
