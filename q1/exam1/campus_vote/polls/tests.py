from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


class PollsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.q1 = Question.objects.create(
            title="是否需要增設飲水機？",
            pub_date=timezone.now(),
            description="校園裡的飲水機不夠用，是否要增設更多飲水機？",
            is_open=True,
        )
        cls.c1 = Choice.objects.create(question=cls.q1, choice_text="非常需要", votes=12)
        cls.c2 = Choice.objects.create(question=cls.q1, choice_text="目前沒有需求", votes=3)

        cls.q2 = Question.objects.create(
            title="校園網路是否改為雙語進行？",
            pub_date=timezone.now(),
            description="希望提升國際參與度。",
            is_open=False,
        )
        Choice.objects.create(question=cls.q2, choice_text="全部雙語", votes=8)

    def test_question_model_content(self):
        self.assertEqual(self.q1.title, "是否需要增設飲水機？")
        self.assertTrue(self.q1.is_open)
        self.assertEqual(self.q1.description, "校園裡的飲水機不夠用，是否要增設更多飲水機？")

    def test_choice_model_content(self):
        self.assertEqual(self.c1.choice_text, "非常需要")
        self.assertEqual(self.c1.votes, 12)

    def test_question_str(self):
        self.assertEqual(str(self.q1), "是否需要增設飲水機？")

    def test_choice_str(self):
        self.assertEqual(str(self.c1), "非常需要")

    def test_foreign_key_relation(self):
        self.assertEqual(self.c1.question, self.q1)
        self.assertEqual(self.q1.choices.count(), 2)

    def test_home_url_by_path(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_url_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertTemplateUsed(response, "base.html")

    def test_home_contains_seeded_data(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "是否需要增設飲水機？")
        self.assertContains(response, "非常需要")
        self.assertContains(response, "目前沒有需求")

    def test_question_detail_url_by_path(self):
        response = self.client.get(f"/question/{self.q1.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_question_detail_url_by_name(self):
        response = self.client.get(reverse("question_detail", args=[self.q1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "question_detail.html")
        self.assertContains(response, "校園裡的飲水機不夠用")

    def test_stats_url_and_content(self):
        response = self.client.get(reverse("stats"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stats.html")
        self.assertContains(response, "問題總數")
        self.assertContains(response, "2")  # 兩筆 question

    def test_stats_open_count(self):
        response = self.client.get(reverse("stats"))
        self.assertContains(response, "開放中的問題數")
        self.assertContains(response, "非常需要")  # q1 的最高票選項

    def test_question_not_found(self):
        response = self.client.get(reverse("question_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)
