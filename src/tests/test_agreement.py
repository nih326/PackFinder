from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from base.models import Profile, ChatRoom, Message
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

class AgreementTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.user1 = get_user_model().objects.create_user(
            email='user1@ncsu.edu',
            password='testpass123'
        )
        cls.user2 = get_user_model().objects.create_user(
            email='user2@ncsu.edu',
            password='testpass123'
        )
        cls.user3 = get_user_model().objects.create_user(
            email='user3@ncsu.edu',
            password='testpass123'
        )

        # Create user profiles with preferences
        cls.user1.profile.name = "User One"
        cls.user1.profile.sleep_schedule = 1
        cls.user1.profile.cleanliness = 2
        cls.user1.profile.course = "Computer Science"
        cls.user1.profile.save()

        cls.user2.profile.name = "User Two"
        cls.user2.profile.sleep_schedule = 2
        cls.user2.profile.cleanliness = 3
        cls.user2.profile.degree = "Masters"
        cls.user2.profile.save()

        cls.user3.profile.name = "User Three"
        cls.user3.profile.sleep_schedule = 1
        cls.user3.profile.cleanliness = 2
        cls.user3.profile.diet = "Vegetarian"
        cls.user3.profile.save()

        cls.findpeople_url = reverse('findpeople')

    def test_generate_roommate_agreement(self):
        """Test that new chat room is created from profile"""
        chatroom = ChatRoom.objects.create()
        chatroom.participants.add(self.user1, self.user2)
        self.client.login(email='user1@ncsu.edu', password='testpass123')

        response = self.client.get(reverse('roommate_agreement', kwargs={'email': self.user2.email}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/roommate_agreement.html')

    def test_preferences_user1(self):
        """Test that the preferences are getting displayed correctly for User 1"""
        chatroom = ChatRoom.objects.create()
        chatroom.participants.add(self.user1, self.user2)
        self.client.login(email='user1@ncsu.edu', password='testpass123')

        response = self.client.get(reverse('roommate_agreement', kwargs={'email': self.user2.email}))
        self.assertContains(response, self.user1.profile.get_sleep_schedule_display())
        self.assertContains(response, self.user1.profile.get_cleanliness_display())
        self.assertContains(response, self.user1.profile.get_noise_preference_display())
        self.assertContains(response, self.user1.profile.get_guest_preference_display())

    def test_preferences_user2(self):
        """Test that the preferences are getting displayed correctly for User 2"""
        chatroom = ChatRoom.objects.create()
        chatroom.participants.add(self.user1, self.user2)
        self.client.login(email='user1@ncsu.edu', password='testpass123')

        response = self.client.get(reverse('roommate_agreement', kwargs={'email': self.user2.email}))
        self.assertContains(response, self.user2.profile.get_sleep_schedule_display())
        self.assertContains(response, self.user2.profile.get_cleanliness_display())
        self.assertContains(response, self.user2.profile.get_noise_preference_display())
        self.assertContains(response, self.user2.profile.get_guest_preference_display())
