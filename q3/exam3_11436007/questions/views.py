from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Question, Comment
from .forms import QuestionForm, TeacherManageForm, SecretaryManageForm, CommentForm


def _get_user_role(user):
    if not user.is_authenticated:
        return None
    groups = set(user.groups.values_list('name', flat=True))
    if 'Teacher' in groups:
        return 'teacher'
    if 'Secretary' in groups:
        return 'secretary'
    if 'Student' in groups:
        return 'student'
    return None


def question_list(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'questions/question_list.html', {'questions': questions})


def question_open_list(request):
    questions = Question.objects.filter(status='Open').order_by('-created_at')
    return render(request, 'questions/question_open_list.html', {'questions': questions})


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    user = request.user
    role = _get_user_role(user)
    is_author = user.is_authenticated and question.author == user
    return render(request, 'questions/question_detail.html', {
        'question': question,
        'can_edit': is_author,
        'can_delete': is_author,
        'can_manage': role in ('teacher', 'secretary'),
    })


@login_required
def question_create(request):
    # 依權限表：只有 Student 可以在網站建立 question
    if _get_user_role(request.user) != 'student':
        raise Http404
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.status = 'Open'
            question.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm(initial={'course_code': 'DJANGO-11436007'})
    return render(request, 'questions/question_form.html', {'form': form, 'action': 'Create'})


@login_required
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.author != request.user:
        raise Http404
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'questions/question_form.html', {'form': form, 'action': 'Edit'})


@login_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.author != request.user:
        raise Http404
    if request.method == 'POST':
        question.delete()
        return redirect('question_list')
    return render(request, 'questions/question_confirm_delete.html', {'question': question})


@login_required
def question_manage(request, pk):
    question = get_object_or_404(Question, pk=pk)
    role = _get_user_role(request.user)
    if role not in ('teacher', 'secretary'):
        raise Http404
    FormClass = TeacherManageForm if role == 'teacher' else SecretaryManageForm
    if request.method == 'POST':
        form = FormClass(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = FormClass(instance=question)
    return render(request, 'questions/question_manage.html', {'form': form, 'question': question, 'role': role})


@login_required
def add_comment(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.author = request.user
            comment.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = CommentForm()
    return render(request, 'questions/comment_form.html', {'form': form, 'question': question})
