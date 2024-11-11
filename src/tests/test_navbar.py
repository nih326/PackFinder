from django.test import TestCase
from django.urls import reverse


class NavbarTests(TestCase):
    def test_navbar_unauthenticated_links(self):
        """Test that unauthenticated users see correct nav links"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/about"')
        self.assertContains(response, 'href="/signup"')
        self.assertNotContains(response, 'href="/profile"')
        self.assertNotContains(response, 'href="/myroom"')
        self.assertNotContains(response, 'href="/findpeople"')
        self.assertNotContains(response, 'href="/user_logout"')

    def test_navbar_brand_link(self):
        """Test that the PackFinder brand link is present"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, '🐺 PackFinder')
        self.assertContains(response, 'href="/"')

    def test_about_link_always_visible(self):
        """Test that the About link is always visible regardless of auth status"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'href="/about"')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'href="/about"')
