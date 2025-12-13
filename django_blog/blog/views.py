from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import (
    FormView,
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin

from .forms import (
    UserRegistrationForm,
    UserUpdateForm,
    ProfileUpdateForm,
    PostCreationForm,
    PostUpdateForm,
)
from .models import Profile, Post, Comment


class RegisterView(FormView):
    template_name = "blog/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("blog:profile")
    http_method_names = ["get", "post"]

    def form_valid(self, form):
        # save user, log them in, show a message
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["method"] = self.request.method
        return context


class ProfileView(LoginRequiredMixin, View):
    template_name = "blog/profile.html"
    login_url = reverse_lazy("blog:login")
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
        return render(
            request,
            self.template_name,
            {
                "u_form": u_form,
                "p_form": p_form,
                "profile": profile,
                "method": request.method,
            },
        )

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("blog:profile")
        # If invalid re-render with errors
        return render(
            request,
            self.template_name,
            {
                "u_form": u_form,
                "p_form": p_form,
                "profile": profile,
                "method": request.method,
            },
        )


class UserLoginView(LoginView):
    template_name = "blog/login.html"


class UserLogoutView(LogoutView):
    template_name = "blog/logout.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/postdetail.html"
    context_object_name = "post"

    def get_queryset(self):
        # fetches author in same query
        return super().get_queryset().select_related("author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # provide recent posts for sidebar or related lists
        context["recent_posts"] = Post.objects.order_by("-published_date")[:5]
        return context


class PostListView(ListView):
    model = Post
    template_name = "blog/postlist.html"
    context_object_name = "posts"
    paginate_by = 10
    queryset = Post.objects.select_related("author").order_by("-published_date")


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostCreationForm
    template_name = "blog/newpost.html"
    success_url = reverse_lazy("blog:post-list")
    success_message = "Post created successfully."

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = Post
    form_class = PostUpdateForm
    template_name = "blog/editpost.html"
    success_url = reverse_lazy("blog:post-list")
    success_message = "Post updated successfully."

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post-list")

    def test_func(self):
        return self.get_object().author == self.request.user


class CommentListView(ListView):
    model = Comment
    template_name = "blog/listcomment.html"
    context_object_name = "comments"

    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk")
        qs = Comment.objects.all().order_by("-id")
        if post_pk:
            qs = qs.filter(post_id=post_pk)
        return qs


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["body"]  # adjust if your Comment field name differs
    template_name = "blog/create_comment.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        post_pk = self.kwargs.get("post_pk") or self.request.POST.get("post_pk")
        form.instance.post = get_object_or_404(Post, pk=post_pk)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.object.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ["body"]
    template_name = "blog/edit_comment.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/delete_comment.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.object.post.pk})
