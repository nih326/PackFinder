from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from base.models import Profile
import random


class UserSeedingCommandTests(TestCase):
    @patch('django.core.mail.send_mail')
    def test_user_seeding_success(self, mock_send_mail):
        """Test the user seeding command successfully creates users and sends email notification."""
        # Mocking email sending
        mock_send_mail.return_value = 1  


        call_command('seed_users', 5)


        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 5)


        profiles = Profile.objects.all()
        self.assertEqual(profiles.count(), 5)

        mock_send_mail.assert_called_once_with(
            'New Users Added to the Platform',
            'The following new users were added to the platform:\n\n' +
            "\n\n".join([f"Name: {user.first_name} {user.last_name}\nEmail: {user.email}\nGender: {profile.gender}\nDegree: {profile.degree}\nDiet: {profile.diet}\nCourse: {profile.course}\nBio: {profile.bio}\nBirth Date: {profile.birth_date}\nHometown: {profile.hometown}\nCountry: {profile.country}\nPreference - Gender: {profile.preference_gender}, Degree: {profile.preference_degree}, Diet: {profile.preference_diet}, Course: {profile.preference_course}\nProfile Complete: {profile.is_profile_complete}" for user, profile in zip(users, profiles)]),
            'sanjananshreenivas@gmail.com',
            ['sanjanashreenivas1399@gmail.com']
        )

    @patch('django.core.mail.send_mail')
