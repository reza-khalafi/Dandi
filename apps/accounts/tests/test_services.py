from django.test import TestCase
from django.contrib.auth.models import User
from apps.accounts.services.auth_service import AuthService
from apps.accounts.repositories.user_repository import UserRepository


class AuthServiceTests(TestCase):
    def setUp(self):
        self.auth_service = AuthService()

    def test_register_user_success(self):
        user = self.auth_service.register_user(
            username='newuser',
            password='secretpassword123',
            email='newuser@example.com'
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(user.check_password('secretpassword123'))
        self.assertTrue(UserRepository.exists_by_username('newuser'))

    def test_authenticate_user_valid(self):
        self.auth_service.register_user(
            username='authuser',
            password='validpassword123'
        )
        authenticated = self.auth_service.authenticate_user(
            request=None,
            username='authuser',
            password='validpassword123'
        )
        self.assertIsNotNone(authenticated)
        self.assertEqual(authenticated.username, 'authuser')

    def test_authenticate_user_invalid(self):
        self.auth_service.register_user(
            username='authuser2',
            password='validpassword123'
        )
        authenticated = self.auth_service.authenticate_user(
            request=None,
            username='authuser2',
            password='wrongpassword'
        )
        self.assertIsNone(authenticated)
