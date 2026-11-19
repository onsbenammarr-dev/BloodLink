from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import User


class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "role")


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form = AddUserForm
    ordering = ("email",)
    list_display = ("email", "role", "is_active")
    search_fields = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Infos", {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "role", "password1", "password2")}),
    )