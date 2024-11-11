from django.core.management.base import BaseCommand
from base.models import CustomUser  # Adjust the import based on your project structure

class Command(BaseCommand):
    help = 'Delete specified users'

    def add_arguments(self, parser):
        parser.add_argument('usernames', nargs='+', help='Emails to delete')

    def handle(self, *args, **kwargs):
        emails = kwargs['usernames']
        deleted_count, _ = CustomUser.objects.filter(email__in=emails).delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_count} user(s).'))
