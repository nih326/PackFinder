from django.test import TestCase
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import HttpRequest
from unittest.mock import patch

class CampusLifeTests(TestCase):
    
    def test_campus_life_page_loads(self):
        """Test that the campus life page loads successfully and uses the correct template."""
        response = self.client.get(reverse('campus_life')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/campus_life.html')

    def test_campus_life_page_content(self):
        """Test that the campus life page contains specific text."""
        response = self.client.get(reverse('campus_life'))
        self.assertContains(response, "Campus Life: Tips and Discussions")
        self.assertContains(response, "Discuss all things related to Campus Life here!")
