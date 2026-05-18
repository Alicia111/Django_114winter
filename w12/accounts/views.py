from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import CustomUserCreationForm


# Extra extension: built-in Groups drive role-specific homepage sections.
# The manager assigns Student, Teacher, or Assistant in the admin Users page.
ROLE_CARDS = {
    "Student": "Student view: read course materials and check homework reminders.",
    "Teacher": "Teacher view: prepare lessons and review class progress.",
    "Assistant": "Assistant view: support students and collect common questions.",
}


# HomeView adds role_cards from the user's Groups.
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


# Ch10 builds signup with CreateView and redirects to Django's built-in login page.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
