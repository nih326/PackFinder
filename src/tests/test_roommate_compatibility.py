from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from base.models import Profile


class RoommateCompatibilityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users and profiles
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

        # User 1 profile
        cls.user1_profile = Profile.objects.create(
            user=cls.user1,
            name="User One",
            gender="Female",
            diet="Vegetarian",
            degree="Masters",
            course="Computer Science",
            country="USA",
            gender_preference="No Preference",
            diet_preference="No Preference",
            degree_preference="No Preference",
            course_preference="No Preference",
            country_preference="No Preference"
        )

        # User 2 profile
        cls.user2_profile = Profile.objects.create(
            user=cls.user2,
            name="User Two",
            gender="Male",
            diet="Non-Vegetarian",
            degree="Masters",
            course="Data Science",
            country="USA"
        )

        # User 3 profile
        cls.user3_profile = Profile.objects.create(
            user=cls.user3,
            name="User Three",
            gender="Female",
            diet="Vegetarian",
            degree="Bachelors",
            course="Computer Science",
            country="India"
        )

        cls.myroom_url = reverse('myroom')

    def test_compatibility_calculation(self):
        """Test the compatibility calculation between two profiles."""
        from base.views import calculate_compatibility

        score1 = calculate_compatibility(self.user1_profile, self.user2_profile)
        score2 = calculate_compatibility(self.user1_profile, self.user3_profile)

        # User 1 and User 2 have all "No Preference" for User 1
        self.assertGreaterEqual(score1, 50)

        # User 1 and User 3 share multiple matches
        self.assertGreaterEqual(score2, 50)
        self.assertGreater(score2, score1)

    def test_myroom_page_authenticated_user(self):
        """Test that the myroom page loads correctly for an authenticated user."""
        self.client.login(email='user1@ncsu.edu', password='testpass123')

        response = self.client.get(self.myroom_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/myroom.html')
        self.assertContains(response, "Compatibility")
        self.assertContains(response, "User Two")
        self.assertContains(response, "User Three")

    def test_myroom_page_no_compatibility(self):
        """Test that the myroom page shows no compatible profiles when threshold is high."""
        # Modify user1 preferences to exclude all matches
        self.user1_profile.gender_preference = "Male"
        self.user1_profile.diet_preference = "Non-Vegetarian"
        self.user1_profile.degree_preference = "PhD"
        self.user1_profile.save()

        self.client.login(email='user1@ncsu.edu', password='testpass123')
        response = self.client.get(self.myroom_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No compatible profiles found.")
