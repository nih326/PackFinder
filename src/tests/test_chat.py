from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from base.models import Profile, ChatRoom, Message


class ChatRoomTests(TestCase):
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

    def test_create_chat_room_new(self):
        """Test that new chat room is created from profile"""
        self.client.login(email='user1@ncsu.edu', password='testpass123')
        response = self.client.post(reverse('create_chat_room', kwargs={'email': self.user2.email}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ChatRoom.objects.filter(participants=self.user1).filter(participants=self.user2).exists())

    def test_redirect_to_existing_chat_room(self):
        """Test redirection to an existing chat room."""
        chatroom = ChatRoom.objects.create()
        chatroom.participants.add(self.user1, self.user2)

        self.client.login(email='user1@ncsu.edu', password='testpass123')

        # Try to create a chat room with the same participant
        response = self.client.post(reverse('create_chat_room', kwargs={'email': self.user2.email}))

        # Verify redirection to the existing chat room
        self.assertRedirects(response, reverse('chat_room', kwargs={'room_id': chatroom.id}))

    def test_message_sent(self):
        """Test whether message is being sent"""
        chatroom = ChatRoom.objects.create()
        chatroom.participants.add(self.user1, self.user2)

        self.client.login(email='user1@ncsu.edu', password='testpass123')

        # Try to create a chat room with the same participant
        Message.objects.create(room=chatroom, sender=self.user1, content="Hello!")

        # Log in as the second user and check if the message is visible
        self.client.logout()  # Logout first user
        self.client.login(email='user2@ncsu.edu', password='testpass123')
        response = self.client.post(reverse('chat_room', kwargs={'room_id': chatroom.id}))

        # Assert that the response contains the message content
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello!")

    def test_clear_chat(self):
        """Test clear chat functionality"""
        chatroom = ChatRoom.objects.create()
        chatroom.participants.add(self.user1, self.user2)

        self.client.login(email='user1@ncsu.edu', password='testpass123')

        # Try to create a chat room with the same participant
        Message.objects.create(room=chatroom, sender=self.user1, content="Hello!")
        response = self.client.post(reverse("clear_chat", kwargs={'room_id': chatroom.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(chatroom.messages.exclude(sender=None).count(), 0)

    def test_back_to_chats_button(self):
        """Test that clicking 'Back to Chats' button redirects to the correct page."""

        chatroom = ChatRoom.objects.create()
        chatroom.participants.add(self.user1, self.user2)
        self.client.login(email='user1@ncsu.edu', password='testpass123')

        # Simulate clicking 'Back to Chats' button by sending a GET request
        response = self.client.get(reverse('chat_list'))

        # Check that the user is redirected to the chat list page
        self.assertTemplateUsed(response, 'chat/chat_list.html')  # Update template name if different

    def test_chat_with_email_display(self):
        """Test that the email of the other participant is displayed correctly."""
        chatroom = ChatRoom.objects.create()
        chatroom.participants.add(self.user1, self.user2)
        self.client.login(email='user1@ncsu.edu', password='testpass123')

        # Get the URL for the specific chat room
        response = self.client.get(reverse('chat_room', kwargs={'room_id': chatroom.id}))

        # Check if the email of the other participant is correctly displayed
        self.assertContains(response, 'Chat with user2@ncsu.edu')  # Ensure user2's email is displayed
