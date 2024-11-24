from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from base.models import Profile


class FindPeopleTests(TestCase):
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
        cls.user1.profile.gender = "Female"
        cls.user1.profile.sleep_schedule = 1
        cls.user1.profile.cleanliness = 2
        cls.user1.profile.course = "Computer Science"
        cls.user1.profile.save()

        cls.user2.profile.name = "User Two"
        cls.user1.profile.gender = "Female"
        cls.user2.profile.sleep_schedule = 2
        cls.user2.profile.cleanliness = 3
        cls.user2.profile.degree = "Masters"
        cls.user2.profile.save()

        cls.user3.profile.name = "User Three"
        cls.user1.profile.gender = "Female"
        cls.user3.profile.sleep_schedule = 1
        cls.user3.profile.cleanliness = 2
        cls.user3.profile.diet = "Vegetarian"
        cls.user3.profile.save()
        cls.findpeople_url = reverse('findpeople')


    def test_findpeople_page_loads(self):
        """Test that the findpeople page loads correctly."""
        self.client.login(email='user1@ncsu.edu', password='testpass123')
        response = self.client.get(self.findpeople_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/findpeople.html')  # Update template name if different

    def test_preferences_are_saved_correctly(self):
        """Test that user preferences are saved correctly."""
        user1_profile = Profile.objects.get(user=self.user1)
        self.assertEqual(user1_profile.sleep_schedule, 1)
        self.assertEqual(user1_profile.cleanliness, 2)

    def test_filter_returns_correct_results(self):
        """Test that filtering by preferences returns the expected matches."""
        self.client.login(email='user1@ncsu.edu', password='testpass123')

        # Fetch results for user1's preferences
        response = self.client.get(self.findpeople_url, {'gender': [''], 'degree': ['Masters'], 'course': [''], 'diet': [''], 'country': ['']})

        # User3 should match the preferences
        self.assertContains(response, 'User Two')
        # User2 should not match
        self.assertNotContains(response, 'User One')
        self.assertNotContains(response, 'User Three')

    def test_filter_with_no_matches(self):
        """Test that filtering with preferences not matching any user returns no results."""
        self.client.login(email='user1@ncsu.edu', password='testpass123')

        # Use preferences that do not match any user
        response = self.client.get(self.findpeople_url, {'gender': [''], 'degree': ['Masters'], 'course': ['Mechanical Engineering'], 'diet': ['Non Vegetarian'], 'country': ['']})

        # Assert no results are returned
        self.assertNotContains(response, 'User One')
        self.assertNotContains(response, 'User Two')
        self.assertNotContains(response, 'User Three')

    def test_filter_combination_of_preferences(self):
        """Test various combinations of preferences."""
        self.client.login(email='user1@ncsu.edu', password='testpass123')

        # Case 1: Match sleep_schedule = 1 and cleanliness = 2
        response = self.client.get(self.findpeople_url, {'gender': [''], 'degree': [''], 'course': [''], 'diet': ['Vegetarian'], 'country': ['']})
        self.assertContains(response, 'User Three')

    def test_preferences_display_user1(self):
        """Test various combinations of preferences."""
        self.client.login(email='user1@ncsu.edu', password='testpass123')

        # Case 1: Match sleep_schedule = 1 and cleanliness = 2
        response = self.client.get(self.findpeople_url)
        self.assertContains(response, self.user2.profile.get_preference_degree_display())
        self.assertContains(response, self.user3.profile.get_preference_diet_display())

    def test_preferences_display_user2(self):
        """Test various combinations of preferences."""
        self.client.login(email='user1@ncsu.edu', password='testpass123')

        # Case 1: Match sleep_schedule = 1 and cleanliness = 2
        response = self.client.get(self.findpeople_url)
        self.assertContains(response, self.user1.profile.get_preference_course_display())
        self.assertContains(response, self.user3.profile.get_preference_diet_display())

    def test_preferences_display_user3(self):
        """Test various combinations of preferences."""
        self.client.login(email='user1@ncsu.edu', password='testpass123')

        # Case 1: Match sleep_schedule = 1 and cleanliness = 2
        response = self.client.get(self.findpeople_url)
        self.assertContains(response, self.user1.profile.get_preference_course_display())
        self.assertContains(response, self.user2.profile.get_preference_degree_display())

    def test_profile_display_user1(self):
        """Test various combinations of preferences."""
        self.client.login(email='user1@ncsu.edu', password='testpass123')

        # Case 1: Match sleep_schedule = 1 and cleanliness = 2
        response = self.client.get(self.findpeople_url)
        self.assertContains(response, self.user2.profile.name)
        self.assertContains(response, self.user2.profile.get_gender_display())

        self.assertContains(response, self.user3.profile.name)
        self.assertContains(response, self.user3.profile.get_gender_display())

    def test_profile_display_user2(self):
        """Test various combinations of preferences."""
        self.client.login(email='user2@ncsu.edu', password='testpass123')

        # Case 1: Match sleep_schedule = 1 and cleanliness = 2
        response = self.client.get(self.findpeople_url)
        self.assertContains(response, self.user1.profile.name)
        self.assertContains(response, self.user1.profile.get_gender_display())

        self.assertContains(response, self.user3.profile.name)
        self.assertContains(response, self.user3.profile.get_gender_display())


    def test_profile_display_user3(self):
        """Test various combinations of preferences."""
        self.client.login(email='user3@ncsu.edu', password='testpass123')

        # Case 1: Match sleep_schedule = 1 and cleanliness = 2
        response = self.client.get(self.findpeople_url)
        self.assertContains(response, self.user1.profile.name)
        self.assertContains(response, self.user1.profile.get_gender_display())

        self.assertContains(response, self.user2.profile.name)
        self.assertContains(response, self.user2.profile.get_gender_display())

    



    

