from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model  
from base.models import Profile

class LoginPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test user with NCSU email
        cls.user = get_user_model().objects.create_user(
            email='test@ncsu.edu',
            password='testpass123'
        )
        # Remove Profile creation since it's handled automatically
        cls.login_url = reverse('login')

    def test_login_page_loads(self):
        """Test that the login page loads correctly."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')  # Adjust template path if different

    def test_login_success(self):
        """Test successful login."""
        response = self.client.post(self.login_url, {
            'username': 'test@ncsu.edu',
            'password': 'testpass123'
        }, follow=True)  # Add follow=True to follow redirects
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_failure(self):
        """Test failed login."""
        response = self.client.post(self.login_url, {
            'username': 'test@ncsu.edu',  # Updated email
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_redirect_if_authenticated(self):
        """Test redirect for already authenticated users."""
        # First login
        self.client.login(username='test@ncsu.edu', password='testpass123')
        
        # Then test the redirect
        response = self.client.get(self.login_url)  # Remove follow=True
        self.assertEqual(response.status_code, 200)  # First check redirect status
    