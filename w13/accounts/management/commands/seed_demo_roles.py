from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


DEMO_PASSWORD = "testpass123"
ROLE_NAMES = ["Student", "Teacher", "Assistant"]


class Command(BaseCommand):
    help = "Create demo groups, a manager account, and sample users."

    def handle(self, *args, **options):
        groups = {
            name: Group.objects.get_or_create(name=name)[0] for name in ROLE_NAMES
        }
        user_model = get_user_model()

        manager, _ = user_model.objects.get_or_create(
            username="manager",
            defaults={
                "email": "manager@example.com",
                "age": 35,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        manager.email = "manager@example.com"
        manager.age = 35
        manager.is_staff = True
        manager.is_superuser = True
        manager.set_password(DEMO_PASSWORD)
        manager.save()

        demo_users = [
            ("student1", "student1@example.com", 20, "Student"),
            ("teacher1", "teacher1@example.com", 40, "Teacher"),
            ("assistant1", "assistant1@example.com", 24, "Assistant"),
        ]
        for username, email, age, group_name in demo_users:
            user, _ = user_model.objects.get_or_create(
                username=username,
                defaults={"email": email, "age": age},
            )
            user.email = email
            user.age = age
            user.set_password(DEMO_PASSWORD)
            user.save()
            user.groups.set([groups[group_name]])

        self.stdout.write(self.style.SUCCESS("Demo roles and users are ready."))
        self.stdout.write("manager / testpass123")
        self.stdout.write("student1 / testpass123")
        self.stdout.write("teacher1 / testpass123")
        self.stdout.write("assistant1 / testpass123")
