from django.conf import settings
from base.models import UserProfile  # Adjust import as needed
from django.utils.timezone import now

from django.utils.crypto import get_random_string

# Generate a unique username
username = "user_" + get_random_string(length=8)
user, created = settings.AUTH_USER_MODEL.objects.get_or_create(
    username=username
)

class Command(BaseCommand):
    help = "Populate the database with sample data"

    def handle(self, *args, **kwargs):
        # Get or create a user
        user, created = settings.AUTH_USER_MODEL.objects.get_or_create(
            username="testuser",  # Replace with the actual test username
            defaults={
                "email": "testuser@example.com",  # Adjust to match fields in your custom user model
                "password": "password123"        # Never store plaintext passwords in production
            }
        )

        if created:
            self.stdout.write(f"Created new user: {user.username}")
        else:
            self.stdout.write(f"Using existing user: {user.username}")

        # Get or create a UserProfile
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "room_status": "offering",
                "name": "Test User",
            }
        )

        if created:
            self.stdout.write(f"Created new UserProfile for user: {user.username}")
        else:
            self.stdout.write(f"Using existing UserProfile for user: {user.username}")

        # Additional logic (e.g., creating rooms) can follow here
