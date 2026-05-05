from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

ROLES = ['指揮中心人員', '醫療人員', '物資人員', '避難所人員']

USERS = [
    {'username': 'commander1', 'email': 'commander1@example.com', 'password': 'pass1234', 'role': '指揮中心人員'},
    {'username': 'medic1',     'email': 'medic1@example.com',     'password': 'pass1234', 'role': '醫療人員'},
    {'username': 'logist1',    'email': 'logist1@example.com',    'password': 'pass1234', 'role': '物資人員'},
    {'username': 'shelter1',   'email': 'shelter1@example.com',   'password': 'pass1234', 'role': '避難所人員'},
]


class Command(BaseCommand):
    help = 'Seed regular users with roles'

    def handle(self, *args, **options):
        for role_name in ROLES:
            Group.objects.get_or_create(name=role_name)
            self.stdout.write(f'  Group: {role_name}')

        for data in USERS:
            if User.objects.filter(username=data['username']).exists():
                self.stdout.write(f'  skip existing: {data["username"]}')
                continue
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                is_staff=False,
                is_superuser=False,
                is_active=True,
            )
            group = Group.objects.get(name=data['role'])
            user.groups.add(group)
            self.stdout.write(self.style.SUCCESS(f'  Created: {user.username} [{data["role"]}]'))

        self.stdout.write(self.style.SUCCESS('Done seeding users.'))
