from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


DEMO_PASSWORD = "testpass123"
ROLE_NAMES = ["Student", "Teacher", "Assistant"]


# Create a manager account, demo users, and Groups for classroom testing.
class Command(BaseCommand):
    help = "Create demo groups, a manager account, and sample users."

    def handle(self, *args, **options):
        # These Groups appear in the admin Users edit page.
        groups = {
            name: Group.objects.get_or_create(name=name)[0] for name in ROLE_NAMES
        }
        user_model = get_user_model()

        # Manager: can log in to /admin/.
        manager, _ = user_model.objects.get_or_create(
            username="manager",
            defaults={
                "email": "manager@example.com",
                "age": 35,
                "address": "台北市中正區忠孝東路一段 1 號",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        manager.email = "manager@example.com"
        manager.age = 35
        manager.address = "台北市中正區忠孝東路一段 1 號"
        manager.is_staff = True
        manager.is_superuser = True
        manager.set_password(DEMO_PASSWORD)
        manager.save()

        # Demo accounts: let students compare role-specific homepage content.
        demo_users = [
            ("student1", "student1@example.com", 20, "新北市板橋區文化路二段 100 號", "Student"),
            ("teacher1", "teacher1@example.com", 40, "桃園市中壢區中央西路 200 號", "Teacher"),
            ("assistant1", "assistant1@example.com", 24, "台中市北區三民路三段 50 號", "Assistant"),
        ]
        for username, email, age, address, group_name in demo_users:
            user, _ = user_model.objects.get_or_create(
                username=username,
                defaults={"email": email, "age": age, "address": address},
            )
            user.email = email
            user.age = age
            user.address = address
            user.set_password(DEMO_PASSWORD)
            user.save()
            user.groups.set([groups[group_name]])

        self.stdout.write(self.style.SUCCESS("Demo roles and users are ready."))
        self.stdout.write("manager / testpass123")
        self.stdout.write("student1 / testpass123")
        self.stdout.write("teacher1 / testpass123")
        self.stdout.write("assistant1 / testpass123")
