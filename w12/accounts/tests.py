from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse


# Verify that CustomUser works without relying on Ch9.
class CustomUserTests(TestCase):
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            username="student",
            email="student@example.com",
            password="testpass123",
            age=21,
        )
        self.assertEqual(user.username, "student")
        self.assertEqual(user.email, "student@example.com")
        self.assertEqual(user.age, 21)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="testpass123",
            age=35,
        )
        self.assertEqual(admin_user.username, "admin")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


# Verify signup, login, logout, and homepage authentication behavior.
class AuthenticationPageTests(TestCase):
    def test_homepage_logged_out(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are not logged in")
        self.assertContains(response, "Log In")
        self.assertContains(response, "Sign Up")
        self.assertTemplateUsed(response, "home.html")

    def test_login_page(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Log In")
        self.assertTemplateUsed(response, "registration/login.html")

    def test_signup_page(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign Up")
        self.assertContains(response, "Email")
        self.assertContains(response, "Age")
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_form_creates_user(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "age": 25,
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertEqual(get_user_model().objects.count(), 1)
        user = get_user_model().objects.get(username="testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.age, 25)

    def test_login_logout_flow(self):
        user = get_user_model().objects.create_user(
            username="flowuser",
            email="flowuser@example.com",
            password="testpass123",
            age=19,
        )

        login_response = self.client.post(
            reverse("login"),
            {
                "username": user.username,
                "password": "testpass123",
            },
        )
        self.assertRedirects(login_response, reverse("home"))

        home_response = self.client.get(reverse("home"))
        self.assertContains(home_response, "Hi flowuser!")
        self.assertContains(home_response, "You are 19 years old.")

        logout_response = self.client.post(reverse("logout"))
        self.assertRedirects(logout_response, reverse("home"))

        logged_out_response = self.client.get(reverse("home"))
        self.assertContains(logged_out_response, "You are not logged in")


# Verify admin Groups, role-specific homepage content, and the demo seed command.
class RolePageTests(TestCase):
    def test_student_group_sees_student_view(self):
        user = get_user_model().objects.create_user(
            username="student_role",
            email="student_role@example.com",
            password="testpass123",
            age=20,
        )
        student_group = Group.objects.create(name="Student")
        user.groups.add(student_group)

        self.client.login(username="student_role", password="testpass123")
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Student view")
        self.assertNotContains(response, "Teacher view")

    def test_staff_user_sees_manager_view(self):
        manager = get_user_model().objects.create_superuser(
            username="manager_role",
            email="manager_role@example.com",
            password="testpass123",
            age=35,
        )

        self.client.login(username=manager.username, password="testpass123")
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Manager view")
        self.assertContains(response, "Open admin")

    def test_user_without_group_sees_no_role_message(self):
        get_user_model().objects.create_user(
            username="no_role",
            email="no_role@example.com",
            password="testpass123",
            age=18,
        )

        self.client.login(username="no_role", password="testpass123")
        response = self.client.get(reverse("home"))

        self.assertContains(response, "No role assigned yet.")

    def test_seed_demo_roles_command(self):
        call_command("seed_demo_roles")

        user_model = get_user_model()
        self.assertTrue(user_model.objects.filter(username="manager").exists())
        self.assertTrue(Group.objects.filter(name="Student").exists())
        self.assertTrue(Group.objects.filter(name="Teacher").exists())
        self.assertTrue(Group.objects.filter(name="Assistant").exists())

        student = user_model.objects.get(username="student1")
        self.assertTrue(student.groups.filter(name="Student").exists())
