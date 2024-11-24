from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from base.models import Profile  # Replace `base` with your app name
from base.forms import ProfileForm  # Replace with the actual form name


class EditProfilePageTests(TestCase):
    def setUp(self):
        # Create a test user and profile
        self.user = User.objects.create_user(
            username="testuser", password="password123", email="testuser@ncsu.edu"
        )
        self.profile = Profile.objects.create(
            user=self.user,
            name="Test User",
            bio="This is a test bio",
            gender="Female",
        )
        self.client.login(username="testuser", password="password123")
        self.url = reverse("edit_profile")  # Replace with the actual URL name

    def test_edit_profile_page_loads(self):
        """Test the Edit Profile page loads successfully."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Profile")
        self.assertTemplateUsed(response, "edit_profile.html")  # Replace with the actual template name

    def test_edit_profile_form_displayed(self):
        """Test the form is displayed on the Edit Profile page."""
        response = self.client.get(self.url)
        self.assertIsInstance(response.context["form"], ProfileForm)
        self.assertContains(response, 'name="name"')  # Field check
        self.assertContains(response, 'name="bio"')  # Field check
        self.assertContains(response, 'type="submit"')  # Save button check

    def test_edit_profile_submission_valid_data(self):
        """Test submitting valid data updates the profile."""
        valid_data = {
            "name": "Updated Name",
            "bio": "Updated bio content",
            "gender": "Male",
        }
        response = self.client.post(self.url, valid_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.name, "Updated Name")
        self.assertEqual(self.profile.bio, "Updated bio content")
        self.assertEqual(self.profile.gender, "Male")

    def test_edit_profile_submission_invalid_data(self):
        """Test submitting invalid data does not update the profile."""
        invalid_data = {
            "name": "",  # Name is required
            "bio": "Updated bio",
            "gender": "NonexistentOption",  # Invalid choice
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Stays on the same page
        self.assertFormError(response, "form", "name", "This field is required.")
        self.assertFormError(response, "form", "gender", "Select a valid choice. NonexistentOption is not one of the available choices.")

    def test_edit_profile_page_unauthenticated_user(self):
        """Test redirect for unauthenticated users."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")
