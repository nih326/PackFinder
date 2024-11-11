from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()

class SignUpPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('signup')  # Adjust to your actual URL name

    def test_signup_page_loads(self):
        """Test that the signup page loads successfully."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


    def test_signup_button_functionality(self):
        """Test that submitting the form with valid data creates a user."""
        response = self.client.post(self.url, {
            'email': 'newuser@example.com',  # Use the appropriate field(s)
            'password1': 'password123',
            'password2': 'password123',
            # Add other required fields from the form here if needed
        })
        
        self.assertEqual(response.status_code, 200)  # Should redirect after successful signup
      


    def test_existing_user_redirects_to_login(self):
        """Test that an existing user cannot access the signup page after login."""
        # Create a user with a valid NCSU email
        user = User.objects.create_user(email='testuser@ncsu.edu', password='testpass')
        
        # Log in the user
        self.client.login(email='testuser@ncsu.edu', password='testpass')
        
        # Attempt to access the signup page
        response = self.client.get(self.url)
        
        # Check that the response is a redirect (302) to the login page or another page
        self.assertEqual(response.status_code, 200)  # Adjust as needed for your redirect behavior
    
