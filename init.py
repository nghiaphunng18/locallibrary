import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "locallibrary.settings")
django.setup()

call_command('makemigrations', 'catalog')
call_command('migrate')
call_command('loaddata', 'sample_data.json')
