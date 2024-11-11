from django.test import TestCase, Client
from django.urls import reverse


class LandingPageTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.landing_page_url = reverse('home')

    def test_landing_page_loads_successfully(self):
        """Test that the landing page loads with a 200 status code"""
        response = self.client.get(self.landing_page_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/landing_page.html')

    def test_hero_section_content(self):
        """Test that the hero section contains the main heading and description"""
        response = self.client.get(self.landing_page_url)
        self.assertContains(response, 'Welcome to PackFinder')
        self.assertContains(response, 'Find the perfect roommate')
        self.assertContains(response, 'hero-section')

    def test_features_section_present(self):
        """Test that all three main features are present"""
        response = self.client.get(self.landing_page_url)
        features = ['Easy Search', 'Connect Seamlessly', 'Build Community']
        for feature in features:
            self.assertContains(response, feature)

    def test_testimonials_section(self):
        """Test that testimonials section is present with user quotes"""
        response = self.client.get(self.landing_page_url)
        self.assertContains(response, 'What Our Users Say')
        test_users = ['Yash', 'Chaitralee', 'Ananya']
        for user in test_users:
            self.assertContains(response, user)

    def test_signup_button_present(self):
        """Test that the sign-up CTA button is present and links correctly"""
        response = self.client.get(self.landing_page_url)
        self.assertContains(response, 'Sign Up Today')
        self.assertContains(response, 'href="/signup/"')

    def test_faq_section_functionality(self):
        """Test that FAQ section contains all questions and toggle functionality"""
        response = self.client.get(self.landing_page_url)
        faq_questions = [
            'What is PackFinder?',
            'How does PackFinder match me with roommates?',
            'Is PackFinder only for NC State students?'
        ]
        for question in faq_questions:
            self.assertContains(response, question)
        self.assertContains(response, 'toggleFaq')
