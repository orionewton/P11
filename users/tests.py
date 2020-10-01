from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


# Create your tests here.


class UserViewTests(TestCase):

    def setUp(self):
        User.objects.create(username='testuser', password="password")

    def test_login(self):
        response = self.client.post(reverse('login'),
                                    {'username': 'testuser',
                                     'password': 'password'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post(reverse('register'),
                                    {'username': 'testuser',
                                     'email': 'testuser@email.com',
                                     'password1': 'password',
                                     'password2': 'password'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('profile'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_modif(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('profile'), {'username': 'test',
                                                         'email': 'modif@gmail.com'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='testuser', password='password')
        self.client.logout()
        self.assertRaises(
            KeyError, lambda: self.client.session['_auth_user_id'])
