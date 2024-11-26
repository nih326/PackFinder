from django.test import TestCase
from unittest.mock import patch
from django.core.management import call_command
from django.test.utils import override_settings


class SeedUsersEmailTests(TestCase):
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    @patch('base.management.commands.seed_users.send_mail')
    def test_send_notification_called(self, mock_send_mail):
        """
        Test that the send_admin_notification function is called with correct arguments
        when users are created.
        """
        user_count = 2

        call_command('seed_users', user_count)
        self.assertTrue(mock_send_mail.called)
        self.assertEqual(mock_send_mail.call_count, 1)

        args, kwargs = mock_send_mail.call_args
        subject = args[0]
        message = args[1]
        from_email = args[2]
        recipient_list = args[3]

        self.assertEqual(subject, "New Users Added to the Platform")
        self.assertIn("The following new users were added to the platform:", message)
        self.assertEqual(from_email, "sanjananshreenivas@gmail.com")
        self.assertEqual([email.strip() for email in recipient_list], ["sanjanashreenivas1399@gmail.com"])
