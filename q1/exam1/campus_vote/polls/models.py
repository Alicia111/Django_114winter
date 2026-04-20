from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    description = models.TextField()
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
