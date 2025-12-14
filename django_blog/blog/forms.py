from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Tag


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="A valid email address is required.",
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
    )

    class Meta:
        model = User
        fields = ("username", "email")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("image", "bio")


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Comma-separated tags (e.g. django, python). New tags will be created.",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "django, python"}
        ),
    )

    class Meta:
        model = Post
        fields = ("title", "contents", "tags")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "contents": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["tags"].initial = ", ".join(
                [t.name for t in self.instance.tags.all()]
            )

    def save(self, commit=True):
        tags_str = self.cleaned_data.pop("tags", "")
        post = super().save(commit=commit)
        # process tags (create if missing)
        tag_names = [t.strip() for t in tags_str.split(",") if t.strip()]
        tags = []
        for name in tag_names:
            obj = Tag.objects.filter(name__iexact=name).first()
            if not obj:
                obj = Tag.objects.create(name=name)
            tags.append(obj)
        post.tags.set(tags)
        return post


# keep aliases used by your views
class PostCreationForm(PostForm):
    class Meta(PostForm.Meta):
        pass


class PostUpdateForm(PostForm):
    class Meta(PostForm.Meta):
        pass


class CommentForm(forms.ModelForm):
    model = Comment
    fields = "content"


class CommentUpdateForm(forms.ModelForm):
    model = Comment
    fields = "content"
