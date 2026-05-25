from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


# Make the Users page in /admin/ work with age and Groups.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "username",
        "email",
        "age",
        "address",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("age", "address")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("email", "age", "address")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
