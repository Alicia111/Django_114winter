from django.contrib import admin
from .models import Post, Author


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "body",
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "bio",
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
