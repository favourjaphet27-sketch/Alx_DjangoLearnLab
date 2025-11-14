from django import forms
from django.contrib.auth import get_user_model


def get_user_creation_form():
    # lazy import to avoid triggering get_user_model() at import time
    from django.contrib.auth.forms import UserCreationForm

    class CustomUserCreationForm(UserCreationForm):
        pass

    return CustomUserCreationForm


def get_user_register_form():
    UserCreationForm = get_user_creation_form()

    class UserRegisterForm(UserCreationForm):
        email = forms.EmailField(required=True)

        class Meta(UserCreationForm.Meta):
            model = get_user_model()
            fields = ["username", "email", "password1", "password2"]

    return UserRegisterForm
