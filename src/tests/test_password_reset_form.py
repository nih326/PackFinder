from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model

class PasswordResetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = get_user_model().objects.create_user(
            email='test@ncsu.edu',
            password='testpass123'
        )
        cls.password_reset_url = reverse('password_reset')
        
    def test_password_reset_page_loads(self):
        """Test that password reset page loads correctly"""
        response = self.client.get(self.password_reset_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')
        
    def test_password_reset_sends_email(self):
        """Test that submitting valid email sends reset email"""
        response = self.client.post(self.password_reset_url, {
            'email': 'test@ncsu.edu'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after success
        self.assertEqual(len(mail.outbox), 1)  # Verify email was sent
        self.assertIn('test@ncsu.edu', mail.outbox[0].to)  # Verify recipient
        
    def test_password_reset_invalid_email(self):
        """Test handling of non-existent email"""
        response = self.client.post(self.password_reset_url, {
            'email': 'nonexistent@ncsu.edu'
        })
        self.assertEqual(response.status_code, 302)  # Should still redirect for security
        self.assertEqual(len(mail.outbox), 0)  # No email should be sent
        
    def test_password_reset_non_ncsu_email(self):
        """Test handling of non-NCSU email"""
        response = self.client.post(self.password_reset_url, {
            'email': 'test@gmail.com'
        })
        self.assertEqual(response.status_code, 302)  # Should return to form
        self.assertEqual(len(mail.outbox), 0)  # No email should be sent
        
    def test_password_reset_empty_email(self):
        """Test handling of empty email submission"""
        response = self.client.post(self.password_reset_url, {
            'email': ''
        })
        self.assertEqual(response.status_code, 200)  # Should return to form
        self.assertFormError(response, 'form', 'email', 'This field is required.')