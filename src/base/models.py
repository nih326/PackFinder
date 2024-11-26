#
# Created on Fri Nov 22 2024
#
# The MIT License (MIT)
# Copyright (c) 2024 Niharika Maruvanahalli Suresh , Diya Shetty, Sanjana Nanjangud Shreenivas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from email.policy import default
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from .utils import check_ncsu_email
from django.conf import settings
from django.contrib.auth.models import User


class CustomUser(AbstractUser):
    """Custom User Model"""

    username = None
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        email = self.email

        if not check_ncsu_email(email):
            raise ValueError("Please use NCSU Email Id!")
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Model for User Profile"""

    GENDER_MALE = "Male"
    GENDER_FEMALE = "Female"
    GENDER_OTHER = "Other"

    DEGREE_BS = "Bachelors"
    DEGREE_MS = "Masters"
    DEGREE_PHD = "Phd"

    DIET_VEG = "Vegetarian"
    DIET_NON_VEG = "Non Vegetarian"

    COURSE_CS = "Computer Science"
    COURSE_CE = "Computer Engineering"
    COURSE_EE = "Electrical Engineering"
    COURSE_MEC = "Mechanical Engineering"

    BLANK = "--"
    NO_PREF = "No Preference"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    DEGREE_CHOICES = (
        (DEGREE_BS, "Bachelors Program (BS)"),
        (DEGREE_MS, "Masters Program (MS)"),
        (DEGREE_PHD, "Post Docterate (PHD)"),
    )

    COURSE_CHOICES = (
        (COURSE_CS, "Computer Science"),
        (COURSE_CE, "Computer Engg."),
        (COURSE_EE, "Electrical Engg."),
        (COURSE_MEC, "Mechanical Engg."),
    )

    DIET_CHOICES = ((DIET_VEG, "Veg"), (DIET_NON_VEG, "Non Veg"))

    PREF_GENDER_CHOICES = (
        (NO_PREF, "No Preference"),
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    PREF_DEGREE_CHOICES = (
        (NO_PREF, "No Preference"),
        (DEGREE_BS, "Bachelors Program (BS)"),
        (DEGREE_MS, "Masters Program (MS)"),
        (DEGREE_PHD, "Post Docterate (PHD)"),
    )

    PREF_DIET_CHOICES = (
        (NO_PREF, "No Preference"),
        (DIET_VEG, "Veg"),
        (DIET_NON_VEG, "Non Veg"),
    )

    PREF_COURSE_CHOICES = (
        (NO_PREF, "No Preference"),
        (COURSE_CS, "Computer Science"),
        (COURSE_CE, "Computer Engg."),
        (COURSE_EE, "Electrical Engg."),
        (COURSE_MEC, "Mechanical Engg."),
    )

    PREFERENCE_CHOICES = [
        (1, "Early Bird (Before 10 PM)"),
        (2, "Night Owl (After 10 PM)"),
        (3, "Flexible"),
    ]

    CLEANLINESS_CHOICES = [
        (1, "Very Neat"),
        (2, "Moderately Clean"),
        (3, "Relaxed"),
    ]

    NOISE_CHOICES = [
        (1, "Very Quiet"),
        (2, "Moderate Noise"),
        (3, "Active/Social"),
    ]

    GUEST_CHOICES = [
        (1, "Rarely/Never"),
        (2, "Occasionally"),
        (3, "Frequently"),
    ]

    IMPORTANCE_CHOICES = [
        (1, "Not Important"),
        (2, "Somewhat Important"),
        (3, "Very Important"),
    ]

    # Add Room Status field
    ROOM_STATUS = [
        ("available", "Looking for Room"),
        ("occupied", "Room Found"),
        ("offering", "Offering Room"),
    ]

    room_status = models.CharField(
        max_length=20, choices=ROOM_STATUS, default="available"
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    """User Profile Model"""
    name = models.CharField(max_length=100, default="")
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    hometown = models.CharField(max_length=100, default="", blank=True)

    gender = models.CharField(
        max_length=128, choices=GENDER_CHOICES, blank=True
    )
    degree = models.CharField(
        max_length=128, choices=DEGREE_CHOICES, blank=True
    )
    diet = models.CharField(max_length=128, choices=DIET_CHOICES, blank=True)
    country = CountryField(blank_label="Select Country", blank=True)
    course = models.CharField(
        max_length=128, choices=COURSE_CHOICES, blank=True
    )

    visibility = models.BooleanField(default=True)
    is_profile_complete = models.BooleanField(default=False)
    profile_photo = models.ImageField(
        default="default.png", upload_to="profile_pics"
    )

    # preferences

    gender_preference = models.CharField(
        max_length=128, choices=PREF_GENDER_CHOICES, default=NO_PREF
    )
    degree_preference = models.CharField(
        max_length=128, choices=PREF_DEGREE_CHOICES, default=NO_PREF
    )
    diet_preference = models.CharField(
        max_length=128, choices=PREF_DIET_CHOICES, default=NO_PREF
    )
    country_preference = CountryField(
        blank_label="No Preference", blank=True, default="No Preference"
    )
    course_preference = models.CharField(
        max_length=128, choices=PREF_COURSE_CHOICES, default=NO_PREF
    )

    email_confirmed = models.BooleanField(default=False)

    # Preferences
    sleep_schedule = models.IntegerField(choices=PREFERENCE_CHOICES, null=True)
    sleep_schedule_importance = models.IntegerField(choices=IMPORTANCE_CHOICES, default=1)

    cleanliness = models.IntegerField(choices=CLEANLINESS_CHOICES, null=True)
    cleanliness_importance = models.IntegerField(choices=IMPORTANCE_CHOICES, default=1)

    noise_preference = models.IntegerField(choices=NOISE_CHOICES, null=True)
    noise_importance = models.IntegerField(choices=IMPORTANCE_CHOICES, default=1)

    guest_preference = models.IntegerField(choices=GUEST_CHOICES, null=True)
    guest_importance = models.IntegerField(
        choices=IMPORTANCE_CHOICES, default=1
    )

    def __str__(self):
        return f"{self.user.email}-profile"


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    """Create User Profile"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    """Save User Profile"""
    instance.profile.save()


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="userprofile",  # Unique related_name for UserProfile
    )
    ROOM_STATUS_CHOICES = [
        ("offering", "Offering"),
        ("available", "Available"),
        ("occupied", "Occupied"),
    ]
    room_status = models.CharField(
        max_length=20, choices=ROOM_STATUS_CHOICES, default="available"
    )
    name = models.CharField(max_length=255)
    degree_preference = models.CharField(max_length=100, blank=True, null=True)
    gender_preference = models.CharField(max_length=10, blank=True, null=True)
    course_preference = models.CharField(max_length=100, blank=True, null=True)
    country_preference = models.CharField(
        max_length=100, blank=True, null=True
    )
    diet_preference = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.user.username


class Room(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="owned_rooms"
    )  # Room owner
    interested_users = models.ManyToManyField(
        Profile,
        related_name="interested_rooms",
        through="Room_interested_users",
        blank=True,
    )
    address = models.CharField(max_length=200)
    rent = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    available_from = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room at {self.address} by {self.owner.name}"


class Room_interested_users(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE
    )  # Foreign key to Room
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE
    )  # Foreign key to Profile
    created_at = models.DateTimeField(auto_now_add=True)  # Optional: Timestamp

    def __str__(self):
        return f"{self.user} interested in {self.room}"


User = get_user_model()


class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name="chat_rooms")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id}"


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"


class MatchPreferences(models.Model):
    profile = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="match_preferences",
    )
    cleanliness = models.IntegerField(
        choices=[(1, "Very Neat"), (2, "Moderately Clean"), (3, "Relaxed")]
    )
    noise_level = models.IntegerField(
        choices=[(1, "Quiet"), (2, "Moderate"), (3, "Loud")]
    )
    guests_frequency = models.IntegerField(
        choices=[(1, "Rarely"), (2, "Sometimes"), (3, "Often")]
    )
    early_bird = models.BooleanField(default=False)
    night_owl = models.BooleanField(default=False)
    smoking_tolerance = models.BooleanField(default=False)
    pet_friendly = models.BooleanField(default=False)

    def __str__(self):
        return f"Preferences of {self.profile.user.email}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    degree_preference = models.CharField(max_length=100, blank=True, null=True)
    gender_preference = models.CharField(max_length=10, blank=True, null=True)
    course_preference = models.CharField(max_length=100, blank=True, null=True)
    country_preference = models.CharField(max_length=100, blank=True, null=True)
    diet_preference = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
