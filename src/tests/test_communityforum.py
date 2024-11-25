from django.test import TestCase
from django.urls import reverse

class ForumPageTests(TestCase):
    def test_forum_page_loads_successfully(self):
        """Test that the forum page loads successfully and contains correct links."""
        response = self.client.get(reverse('forum_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/forum_home.html')  # Update to 'forum/forum_home.html'
        self.assertContains(response, "Community Forum")
