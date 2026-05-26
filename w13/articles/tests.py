from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Article, Comment


class ArticleModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.author = User.objects.create_user(
            username="writer", password="testpass123", age=30
        )
        cls.article = Article.objects.create(
            title="Hello World",
            body="First post.",
            author=cls.author,
        )

    def test_article_str(self):
        self.assertEqual(str(self.article), "Hello World")

    def test_article_get_absolute_url(self):
        self.assertEqual(self.article.get_absolute_url(), f"/articles/{self.article.pk}/")

    def test_comment_belongs_to_article(self):
        comment = Comment.objects.create(
            article=self.article, comment="Nice post", author=self.author
        )
        self.assertEqual(str(comment), "Nice post")
        self.assertIn(comment, self.article.comment_set.all())


class ArticleCRUDPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.author = User.objects.create_user(
            username="author1", password="testpass123", age=28
        )
        cls.other = User.objects.create_user(
            username="other1", password="testpass123", age=22
        )
        cls.article = Article.objects.create(
            title="Campus Update",
            body="Hello class.",
            author=cls.author,
        )

    def test_list_requires_login(self):
        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_list_for_logged_in_user(self):
        self.client.login(username="other1", password="testpass123")
        response = self.client.get(reverse("article_list"))
        self.assertContains(response, "Campus Update")

    def test_detail_for_logged_in_user(self):
        self.client.login(username="other1", password="testpass123")
        response = self.client.get(
            reverse("article_detail", kwargs={"pk": self.article.pk})
        )
        self.assertContains(response, "Hello class.")

    def test_create_sets_author_automatically(self):
        self.client.login(username="other1", password="testpass123")
        response = self.client.post(
            reverse("article_new"),
            {"title": "Auto Author", "body": "Should auto-fill."},
        )
        self.assertEqual(response.status_code, 302)
        article = Article.objects.get(title="Auto Author")
        self.assertEqual(article.author, self.other)


class ArticlePermissionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.author = User.objects.create_user(
            username="owner", password="testpass123", age=35
        )
        cls.intruder = User.objects.create_user(
            username="intruder", password="testpass123", age=20
        )
        cls.article = Article.objects.create(
            title="Mine Only", body="Stay away.", author=cls.author
        )

    def test_author_can_open_edit_page(self):
        self.client.login(username="owner", password="testpass123")
        response = self.client.get(
            reverse("article_edit", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_non_author_cannot_edit(self):
        self.client.login(username="intruder", password="testpass123")
        response = self.client.get(
            reverse("article_edit", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_non_author_cannot_delete(self):
        self.client.login(username="intruder", password="testpass123")
        response = self.client.post(
            reverse("article_delete", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Article.objects.filter(pk=self.article.pk).exists())

    def test_author_can_delete(self):
        self.client.login(username="owner", password="testpass123")
        response = self.client.post(
            reverse("article_delete", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(pk=self.article.pk).exists())


class CommentFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.author = User.objects.create_user(
            username="poster", password="testpass123", age=25
        )
        cls.commenter = User.objects.create_user(
            username="commenter", password="testpass123", age=21
        )
        cls.article = Article.objects.create(
            title="Discuss", body="Drop a comment.", author=cls.author
        )

    def test_detail_page_has_comment_form(self):
        self.client.login(username="commenter", password="testpass123")
        response = self.client.get(
            reverse("article_detail", kwargs={"pk": self.article.pk})
        )
        self.assertContains(response, "Add a comment")

    def test_post_comment_creates_record_with_author(self):
        self.client.login(username="commenter", password="testpass123")
        response = self.client.post(
            reverse("article_detail", kwargs={"pk": self.article.pk}),
            {"comment": "Great article."},
        )
        self.assertEqual(response.status_code, 302)
        comment = Comment.objects.get(comment="Great article.")
        self.assertEqual(comment.author, self.commenter)
        self.assertEqual(comment.article, self.article)


class SeedDemoArticlesCommandTests(TestCase):
    def test_seed_creates_articles_and_comments(self):
        call_command("seed_demo_articles")
        self.assertTrue(Article.objects.filter(title="Campus News").exists())
        self.assertTrue(Article.objects.filter(title="Student Report").exists())
        self.assertEqual(Comment.objects.count(), 2)
