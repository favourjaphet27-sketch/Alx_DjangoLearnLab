from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="A valid email address is required.",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "you@example.com"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("username", "email")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("image", "bio")
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "contents")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "contents": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
        }


class PostCreationForm(PostForm):
    class Meta(PostForm.Meta):
        pass


class PostUpdateForm(PostForm):
    class Meta(PostForm.Meta):
        pass

class CommentForm(forms.ModelForm):
    model = Comment
    fields = ('content')

class CommentUpdateForm(forms.ModelForm):
    model = Comment
    fields = ('content')
