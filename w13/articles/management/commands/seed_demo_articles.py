from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command

from articles.models import Article, Comment


DEMO_PASSWORD = "testpass123"


class Command(BaseCommand):
    help = "Create demo articles and comments for Ch13-15."

    def handle(self, *args, **options):
        call_command("seed_demo_roles")
        user_model = get_user_model()
        student = user_model.objects.get(username="student1")
        teacher = user_model.objects.get(username="teacher1")
        assistant = user_model.objects.get(username="assistant1")

        first_article, _ = Article.objects.get_or_create(
            title="Campus News",
            defaults={
                "body": "The Django class is building a newspaper app.",
                "author": teacher,
            },
        )
        second_article, _ = Article.objects.get_or_create(
            title="Student Report",
            defaults={
                "body": "Students can create, edit, and comment on articles.",
                "author": student,
            },
        )

        Comment.objects.get_or_create(
            article=first_article,
            comment="This article is ready for Ch15 comments.",
            author=student,
        )
        Comment.objects.get_or_create(
            article=second_article,
            comment="Permissions keep each author's article safe.",
            author=assistant,
        )

        self.stdout.write(self.style.SUCCESS("Demo articles and comments are ready."))
        self.stdout.write("Open http://127.0.0.1:8000/articles/")
