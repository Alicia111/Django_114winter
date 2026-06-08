from django import forms
from .models import Question, Comment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body', 'course_code', 'category']


class TeacherManageForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['status']


class SecretaryManageForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'course_code', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [('Closed', 'Closed')]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
