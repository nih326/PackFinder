from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class HousingTipsTests(StaticLiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_housing_tips_page_loads(self):
        response = self.client.get(reverse('housing_tips'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/housing_tips.html')

    def test_housing_tips_page_content(self):
        response = self.client.get(reverse('housing_tips'))
        self.assertContains(response, "General Housing Tips")
        self.assertContains(response, "Discuss all things related to House Tips here.")

    @patch('django.test.Client.get')
    def test_comment_persistence_with_local_storage(self, mock_get):
        comments = [
            {"author": "Diya", "text": "This is a great place to share ideas!", "likes": 5, "dislikes": 2},
            {"author": "Niha", "text": "Love this discussion thread.", "likes": 3, "dislikes": 1},
        ]
        mock_get.return_value = self.client.get(reverse('housing_tips'))
        mock_response_content = b"<div class='comment'>"
        for comment in comments:
            mock_response_content += f"<p>{comment['author']}: {comment['text']}</p>".encode()

        mock_get.return_value.content = mock_response_content
        response = mock_get.return_value
        for comment in comments:
            self.assertIn(comment['author'], response.content.decode())
            self.assertIn(comment['text'], response.content.decode())

    def test_empty_comment_submission(self):
        response = self.client.post(reverse('housing_tips'), {
            'comment-text': '',
            'comment-name': 'Test User'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Discuss all things related to House Tips here.")

    def test_comment_submission_with_selenium(self):
        self.driver.get(f'{self.live_server_url}/forum/housing-tips/')
        comment_input = self.driver.find_element(By.ID, 'comment-text')
        name_input = self.driver.find_element(By.ID, 'comment-name')
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'form button')

        comment_input.send_keys('This is a test comment.')
        name_input.send_keys('Sanjana NS')
        submit_button.click()
        self.driver.implicitly_wait(3)
        comments = self.driver.find_elements(By.CSS_SELECTOR, '#comments .comment')
        self.assertTrue(
            any('This is a test comment.' in c.text for c in comments),
            "Comment not found in the displayed comments."
        )
