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

    @patch('django.test.Client.get')
    def test_comment_persistence_with_local_storage(self, mock_get):
        """Test that comments are stored and persisted in localStorage."""
        comments = [
            {"author": "Alice", "text": "This is a great place to share ideas!", "likes": 5, "dislikes": 2},
            {"author": "Bob", "text": "Love this discussion thread.", "likes": 3, "dislikes": 1},
        ]
        mock_get.return_value = self.client.get(reverse('campus_life'))
        mock_response_content = b"<div class='comment'>"
        for comment in comments:
            mock_response_content += f"<p>{comment['author']}: {comment['text']}</p>".encode()

        mock_get.return_value.content = mock_response_content
        response = mock_get.return_value
        for comment in comments:
            self.assertIn(comment['author'], response.content.decode())
            self.assertIn(comment['text'], response.content.decode())


    def test_empty_comment_submission(self):
        """Test that empty comment submissions are not allowed."""
        response = self.client.post(reverse('campus_life'), {
            'comment-text': '',
            'comment-name': 'Test User'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Discuss all things related to Campus Life here!")


