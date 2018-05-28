import json

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from .models import User, SignUpCode
from .auth import auth_token, passwd_token


class UserTestCase(TestCase):
    """User test case"""

    def setUp(self):
        self.user = User(
            firstName='User',
            middleName='User',
            lastName='User',
            username='user',
            password='p455w0rd',
            birthday='1986-05-12',
            phone='55 4351 8691'
        )
        self.user.set_password('p455w0rd')
        self.user.save()

        self.signup_code = SignUpCode.objects.create(email='user2@mail.org')
        self.client = Client()

    def tearDown(self):
        self.user.delete()
        self.signup_code.delete()

    def test_password_hash(self):
        self.assertTrue(self.user.password.startswith('pbkdf2_sha256'))
        self.assertEqual(len(self.user.password), 78)

    def test_signup_available(self):
        path = reverse('signup-available')

        response = self.client.post(path, json.dumps({
            'username': 'user2'
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signup_mail(self):
        path = reverse('signup-mail')

        response = self.client.post(path, json.dumps({
            'email': 'user2@mail.org'
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signup_check(self):
        path = reverse('signup-check')

        response = self.client.post(path, json.dumps({
            'email': 'user2@mail.org',
            'code': self.signup_code.code
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signup(self):
        path = reverse('accounts-signup')

        response = self.client.post(path, json.dumps({
            'firstName': 'User 2',
            'middleName': 'User 2',
            'lastName': 'User 2',
            'username': 'user2',
            'password': 'p455w0rd',
            'email': 'user2@mail.org',
            'birthday': '1987-06-20',
            'phone': '55 4530 2942',
            'code': self.signup_code.code
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signin(self):
        path = reverse('accounts-signin')

        response = self.client.post(path, json.dumps({
            'username': 'user', 'password': 'p455w0rd'
        }), content_type='application/json')

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in data.keys())

    def test_passwd_change(self):
        path = reverse('passwd-change')
        token = auth_token(self.user)

        response = self.client.post(path, json.dumps({
            'current': 'p455w0rd', 'password': '12345678'
        }), content_type='application/json',
            HTTP_AUTHORIZATION='Token %s' % token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_passwd_mail(self):
        path = reverse('passwd-mail')

        response = self.client.post(path, json.dumps({
            'username': 'user'
        }), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_passwd_check(self):
        path = reverse('passwd-check')
        token = passwd_token(self.user)

        response = self.client.post(path,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token %s' % token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_passwd_reset(self):
        path = reverse('passwd-reset')
        token = passwd_token(self.user)

        response = self.client.post(path, json.dumps({
            'password': 'p455w0rd'
        }), content_type='application/json',
            HTTP_AUTHORIZATION='Token %s' % token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_me_profile_update(self):
        path = reverse('me-profile')
        token = auth_token(self.user)

        response = self.client.patch(path, json.dumps({
            'firstName': 'User',
            'middleName': 'User',
            'lastName': 'User',
            'birthday': '1994-08-14'
        }), content_type='application/json',
            HTTP_AUTHORIZATION='Token %s' % token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list(self):
        path = reverse('user-list')
        token = auth_token(self.user)

        response = self.client.get(
            path,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token %s' % token
        )

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in data.keys())
        self.assertTrue(isinstance(data['results'], list))
