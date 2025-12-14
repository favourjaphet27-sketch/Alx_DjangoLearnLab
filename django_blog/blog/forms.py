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


class TagWidget(forms.TextInput):
    """Simple tag input widget.

    Renders as a normal text input but with a CSS hook and data attribute
    so JavaScript tag pickers (if you add one later) can enhance it.
    """

    template_name = "django/forms/widgets/text.html"

    def __init__(self, attrs=None):
        default_attrs = {
            "class": "form-control tag-widget",
            "placeholder": "django, python",
            "data-role": "tags",
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Comma-separated tags (e.g. django, python). New tags will be created.",
        widget=TagWidget(),
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
