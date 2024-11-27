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

import factory
import random
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.utils import OperationalError
from django.db.models.signals import post_save

from base.models import Profile
from faker import Faker as RealFaker

real_faker = RealFaker()


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    """Faker Factory for User model"""

    class Meta:
        model = get_user_model()

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(
        lambda a: f"{real_faker.first_name().lower()}{random.randint(1000, 9999)}@ncsu.edu"
    )
    is_staff = False


class ProfileFactory(factory.django.DjangoModelFactory):
    """Faker Factory for Profile Model"""

    class Meta:
        model = Profile

    bio = factory.Faker("text")
    birth_date = factory.Faker("date")
    hometown = factory.Faker("city")
    country = factory.Faker("country_code")
    preference_country = factory.Faker("country_code")


class Command(BaseCommand):
    """Django manage.py command"""

    help = "Seed models using fake data"

    def add_arguments(self, parser):
        parser.add_argument("number", nargs="+", type=int)

    def handle(self, *args, **options):
        try:
            number = options["number"][0]
        except BaseException:
            raise CommandError("Please provide the number of users to create.")

        count = number
        users_created = []
        for _ in range(number):
            try:
                user = UserFactory()
                profile = ProfileFactory(user=user)
                profile.name = f"{user.first_name} {user.last_name}"
                profile.gender = random.choices(Profile.GENDER_CHOICES)[0][0]
                profile.degree = random.choices(Profile.DEGREE_CHOICES)[0][0]
                profile.diet = random.choices(Profile.DIET_CHOICES)[0][0]
                profile.course = random.choices(Profile.COURSE_CHOICES)[0][0]

                profile.preference_gender = random.choices(
                    Profile.PREF_GENDER_CHOICES
                )[0][0]
                profile.preference_degree = random.choices(
                    Profile.PREF_DEGREE_CHOICES
                )[0][0]
                profile.preference_diet = random.choices(Profile.PREF_DIET_CHOICES)[0][0]
                profile.preference_course = random.choices(
                    Profile.PREF_COURSE_CHOICES
                )[0][0]
                profile.is_profile_complete = True
                profile.save()
                users_created.append(self.format_user_details(user, profile))

            except OperationalError:
                self.stdout.write(
                    self.style.ERROR(
                        "Please make migrations and migrate. Something went wrong with the DB tables."
                    )
                )
                count = 0
                break
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
                count -= 1

        if users_created:
            self.send_admin_notification(users_created)

        self.stdout.write(self.style.SUCCESS(f"Created {count} User(s)"))

    def format_user_details(self, user, profile):
        """Format user and profile details into a readable string."""
        return (
            f"Name: {user.first_name} {user.last_name}\n"
            f"Email: {user.email}\n"
            f"Gender: {profile.gender}\n"
            f"Degree: {profile.degree}\n"
            f"Diet: {profile.diet}\n"
            f"Course: {profile.course}\n"
            f"Bio: {profile.bio}\n"
            f"Birth Date: {profile.birth_date}\n"
            f"Hometown: {profile.hometown}\n"
            f"Country: {profile.country}\n"
            f"Preference - Gender: {profile.preference_gender}, "
            f"Degree: {profile.preference_degree}, "
            f"Diet: {profile.preference_diet}, "
            f"Course: {profile.preference_course}\n"
            f"Profile Complete: {profile.is_profile_complete}\n"
        )

    def send_admin_notification(self, users_created):
        """Send email notification to the admin about new users."""
        subject = "New Users Added to the Platform"
        message = ("The following new users were added to the platform:\n\n" + "\n\n".join(users_created) + "\n\nThank you!")
        from_email = "sanjananshreenivas@gmail.com"
        recipient_list = ["	sanjanashreenivas1399@gmail.com"]

        try:
            send_mail(subject, message, from_email, recipient_list)
            self.stdout.write(self.style.SUCCESS("Notification email sent to user."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to send email to user: {str(e)}"))
