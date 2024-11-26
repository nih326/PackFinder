import os
import django
from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

class SimpleTest(TestCase):
    def test_settings(self):
        from django.conf import settings
        self.assertTrue(settings.INSTALLED_APPS)
