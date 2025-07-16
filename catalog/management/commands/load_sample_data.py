from datetime import date, timedelta

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
    help = 'Load sample data into the database'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                call_command('loaddata', 'sample_data.json', app_label='catalog')
                self.stdout.write(self.style.SUCCESS('Sample data loaded successfully'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to load data: {e}'))
