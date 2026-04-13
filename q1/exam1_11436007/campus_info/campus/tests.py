from django.test import SimpleTestCase
from django.urls import reverse


class CampusURLTests(SimpleTestCase):
    def test_home_status_code(self):
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)

    def test_clubs_reverse_by_name(self):
        url = reverse("clubs")
        self.assertEqual(url, "/clubs/")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_schedule_uses_template(self):
        response = self.client.get(reverse("schedule"))
        self.assertTemplateUsed(response, "schedule.html")
        self.assertTemplateUsed(response, "base.html")

    def test_faq_contains_category(self):
        response = self.client.get(reverse("faq"))
        self.assertContains(response, "Registration")
        self.assertContains(response, "Questions will be added soon.")

    def test_about_uses_template_and_contains_heading(self):
        response = self.client.get(reverse("about"))
        self.assertTemplateUsed(response, "about.html")
        self.assertContains(response, "About This Site")

    def test_home_contains_sections(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Club Directory")
        self.assertContains(response, "Weekly Schedule")
        self.assertContains(response, "Frequently Asked Questions")
