from django.views.generic import ListView

from .models import Post


class PostList(ListView):
    model = Post
    template_name = "post_list.html"
