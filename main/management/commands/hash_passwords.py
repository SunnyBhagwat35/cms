import json
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Hash passwords in a fixture file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the fixture file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        # Read the fixture file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Hash passwords
        for entry in data:
            if 'password' in entry.get('fields', {}):
                entry['fields']['password'] = make_password(entry['fields']['password'])

        # Update the fixture file with hashed passwords
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

        self.stdout.write(self.style.SUCCESS(f'Passwords in {file_path} have been hashed.'))
