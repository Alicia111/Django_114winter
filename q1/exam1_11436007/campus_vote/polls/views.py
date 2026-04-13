from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .models import Choice, Question


class QuestionListView(ListView):
    model = Question
    template_name = "home.html"
    context_object_name = "questions"
    ordering = ["-pub_date"]


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, "question_detail.html", {"question": question})


def stats(request):
    questions = Question.objects.all()
    top_choices = []
    for q in questions:
        top = q.choices.order_by("-votes").first()
        top_choices.append({"question": q, "top": top})

    context = {
        "question_count": Question.objects.count(),
        "choice_count": Choice.objects.count(),
        "open_count": Question.objects.filter(is_open=True).count(),
        "top_choices": top_choices,
    }
    return render(request, "stats.html", context)
