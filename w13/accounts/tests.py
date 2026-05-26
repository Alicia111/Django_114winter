from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="willy",
            email="willy@example.com",
            password="testpass123",
            age=22,
        )
        self.assertEqual(user.username, "willy")
        self.assertEqual(user.email, "willy@example.com")
        self.assertEqual(user.age, 22)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="superadmin",
            email="super@example.com",
            password="testpass123",
            age=30,
        )
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class AuthenticationPageTests(TestCase):
    def test_home_page_anonymous(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Log In")
        self.assertContains(response, "Sign Up")

    def test_login_page(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Log In")

    def test_signup_page(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign Up")

    def test_signup_form_creates_user(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newbie",
                "email": "newbie@example.com",
                "age": 19,
                "password1": "supersecret123",
                "password2": "supersecret123",
            },
        )
        self.assertEqual(response.status_code, 302)
        User = get_user_model()
        self.assertTrue(User.objects.filter(username="newbie").exists())

    def test_login_then_home_shows_username(self):
        User = get_user_model()
        User.objects.create_user(
            username="alice", password="testpass123", age=25
        )
        self.client.login(username="alice", password="testpass123")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Hi alice")
        self.assertContains(response, "25")


class RolePageTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.student = User.objects.create_user(
            username="stu", password="testpass123", age=20
        )
        student_group, _ = Group.objects.get_or_create(name="Student")
        self.student.groups.add(student_group)

        self.staff = User.objects.create_user(
            username="staffy", password="testpass123", age=33, is_staff=True
        )
        self.no_role = User.objects.create_user(
            username="lonely", password="testpass123", age=18
        )

    def test_student_sees_student_card(self):
        self.client.login(username="stu", password="testpass123")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Student view")

    def test_staff_sees_manager_view(self):
        self.client.login(username="staffy", password="testpass123")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Manager view")

    def test_user_without_group_sees_hint(self):
        self.client.login(username="lonely", password="testpass123")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "No role assigned yet")

    def test_seed_demo_roles_command(self):
        call_command("seed_demo_roles")
        User = get_user_model()
        for username in ("manager", "student1", "teacher1", "assistant1"):
            self.assertTrue(User.objects.filter(username=username).exists())
        self.assertEqual(Group.objects.filter(name="Student").count(), 1)
