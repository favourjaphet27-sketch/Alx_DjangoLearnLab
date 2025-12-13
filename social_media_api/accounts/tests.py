from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowTests(APITestCase):
    def setUp(self):
        self.a = User.objects.create_user(username='a', password='pass')
        self.b = User.objects.create_user(username='b', password='pass2')
        resp = self.client.post('/auth/login/', {'username':'a','password':'pass'}, format='json')
        token = resp.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def test_follow_unfollow(self):
        follow_url = f'/auth/follow/{self.b.id}/'
        unfollow_url = f'/auth/unfollow/{self.b.id}/'

        r = self.client.post(follow_url)
        self.assertEqual(r.status_code, 200)
        self.assertIn(self.b, self.a.following.all())

        r = self.client.post(unfollow_url)
        self.assertEqual(r.status_code, 200)
        self.assertNotIn(self.b, self.a.following.all())
