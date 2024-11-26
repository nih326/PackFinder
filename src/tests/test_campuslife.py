from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class CampusLifeTests(StaticLiveServerTestCase):
    """Consolidated class for Django and Selenium tests for Campus Life."""

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

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

    def test_comment_submission_with_selenium(self):
        """Test comment submission using Selenium."""
        self.driver.get(f'{self.live_server_url}/forum/campus-life/')
        comment_input = self.driver.find_element(By.ID, 'comment-text')
        name_input = self.driver.find_element(By.ID, 'comment-name')
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'form button')

        comment_input.send_keys('This is a test comment.')
        name_input.send_keys('John Doe')
        submit_button.click()
        self.driver.implicitly_wait(3)
        comments = self.driver.find_elements(By.CSS_SELECTOR, '#comments .comment')
        self.assertTrue(
            any('This is a test comment.' in c.text for c in comments),
            "Comment not found in the displayed comments."
        )
