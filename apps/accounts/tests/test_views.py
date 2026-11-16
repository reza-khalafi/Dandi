from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='existinguser',
            password='password123'
        )

    def test_register_view_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_post_success(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'brandnewuser',
            'email': 'brandnew@test.com',
            'password': 'strongpassword123',
            'password_confirm': 'strongpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='brandnewuser').exists())

    def test_register_view_post_mismatched_password(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'mismatchuser',
            'password': 'passwordAAA',
            'password_confirm': 'passwordBBB'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='mismatchuser').exists())

    def test_login_view_get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_post_success(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'existinguser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'existinguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], None, 'نام کاربری یا رمز عبور اشتباه است.')

    def test_logout_view(self):
        self.client.login(username='existinguser', password='password123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
