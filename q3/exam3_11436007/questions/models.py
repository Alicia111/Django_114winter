from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    STATUS_OPEN = 'Open'
    STATUS_ANSWERED = 'Answered'
    STATUS_CLOSED = 'Closed'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_ANSWERED, 'Answered'),
        (STATUS_CLOSED, 'Closed'),
    ]

    CATEGORY_HOMEWORK = 'Homework'
    CATEGORY_PROJECT = 'Project'
    CATEGORY_EXAM = 'Exam'
    CATEGORY_OTHER = 'Other'
    CATEGORY_CHOICES = [
        (CATEGORY_HOMEWORK, 'Homework'),
        (CATEGORY_PROJECT, 'Project'),
        (CATEGORY_EXAM, 'Exam'),
        (CATEGORY_OTHER, 'Other'),
    ]

    title = models.CharField(max_length=200)
    body = models.TextField()
    course_code = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_OTHER)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}: {self.body[:40]}'
