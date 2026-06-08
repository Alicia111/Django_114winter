from django.contrib import admin
from .models import Question, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'course_code', 'created_at']
    list_filter = ['status', 'category']
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'question', 'created_at']
