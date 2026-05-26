from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import CustomUserCreationForm


ROLE_CARDS = {
    "Student": "Student view: read articles and add comments.",
    "Teacher": "Teacher view: create articles and guide class discussion.",
    "Assistant": "Assistant view: support classmates and collect questions.",
}


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["role_cards"] = []
        if user.is_authenticated:
            role_names = set(user.groups.values_list("name", flat=True))
            context["role_cards"] = [
                {"name": name, "message": message}
                for name, message in ROLE_CARDS.items()
                if name in role_names
            ]
        return context


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
