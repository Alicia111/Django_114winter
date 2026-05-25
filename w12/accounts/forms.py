from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


# Signup form: lets users register with username, email, age, and password.
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "age",
            "address",
        )


# Admin change form: lets the manager edit email, age, and address in /admin/.
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "age",
            "address",
        )
