from django.test import TestCase, Client
from django.urls import reverse


class AboutPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.about_url = reverse('about')

    def test_about_page_status_code(self):
        """Test that the about page returns a 200 status code"""
        response = self.client.get(self.about_url)
        self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_template(self):
        """Test that the about page uses the correct template"""
        response = self.client.get(self.about_url)
        self.assertTemplateUsed(response, 'pages/about.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_about_page_contains_title(self):
        """Test that the about page contains the correct title"""
        response = self.client.get(self.about_url)
        self.assertContains(response, '🐺 About')

    def test_about_page_contains_support_email(self):
        """Test that the support email is present on the page"""
        response = self.client.get(self.about_url)
        self.assertContains(response, 'ncsu.packfinder@gmail.com')

    def test_about_page_contains_contributors(self):
        """Test that all contributors are listed on the page"""
        response = self.client.get(self.about_url)
        contributors = [
            'Shandler Mason', 'Teja Varma', 'Kiron Jayesh',
            'Arun Kumar', 'Saigirishwar Rohit Geddam',
            'Ananya Patankar', 'Chaitralee Datar', 'Yash Shah'
        ]
        for contributor in contributors:
            self.assertContains(response, contributor)

    def test_about_page_contains_documentation_link(self):
        """Test that the documentation link is present"""
        response = self.client.get(self.about_url)
        self.assertContains(response, 'https://findmyroomie.readthedocs.io/en/latest/')
        self.assertContains(response, 'Read Documentation')
