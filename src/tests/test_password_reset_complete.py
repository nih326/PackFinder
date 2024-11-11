from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup

class PasswordResetCompleteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password_reset_complete_url = reverse('password_reset_complete')

    def test_page_loads_successfully(self):
        """Test that the password reset complete page loads with the correct status code."""
        response = self.client.get(self.password_reset_complete_url)
        self.assertEqual(response.status_code, 200)

    def test_title_is_correct(self):
        """Test that the title of the page is correct."""
        response = self.client.get(self.password_reset_complete_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title')
        self.assertIsNotNone(title, "Title tag not found")
        self.assertEqual(title.text.strip(), 'Password reset complete')

    def test_main_content(self):
        """Test that main content is present and correct."""
        response = self.client.get(self.password_reset_complete_url)
        content = response.content.decode()

        self.assertIn('Password Reset Complete', content)
        self.assertIn("Your password has been set.", content)
        self.assertIn('/accounts/login/', content)  # Check for the login link

    def test_navigation_elements(self):
        """Test that navigation elements are present."""
        response = self.client.get(self.password_reset_complete_url)
        content = response.content.decode()

        self.assertIn('PackFinder', content)
        self.assertIn('About', content)
        self.assertIn('Sign Up', content)

    def test_footer_elements(self):
        """Test that footer elements are present."""
        response = self.client.get(self.password_reset_complete_url)
        content = response.content.decode()

        self.assertIn('Connect with Us', content)
        self.assertIn('© 2024 PackFinder', content)

    def test_social_media_links(self):
        """Test that social media links are present in the footer."""
        response = self.client.get(self.password_reset_complete_url)
        content = response.content.decode()

        self.assertIn('facebook.com/PackFinder', content)
        self.assertIn('twitter.com/PackFinder', content)
        self.assertIn('instagram.com/PackFinder', content)
        self.assertIn('linkedin.com/company/PackFinder', content)

    def test_styles_and_scripts(self):
        """Test that required styles and scripts are included."""
        response = self.client.get(self.password_reset_complete_url)
        content = response.content.decode()

        self.assertIn('bg-blue-900', content)  # Check navbar background
        self.assertIn('bg-blue-600', content)  # Check button background
        self.assertIn('image.png', content)  # Background image
