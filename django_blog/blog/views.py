from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView, View
from django.urls import reverse_lazy

from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


class RegisterView(FormView):
    template_name = "blog/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("blog:profile")

    def form_valid(self, form):
        # save user, log them in, show a message
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration successful!")
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, View):
    template_name = "blog/profile.html"
    login_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
        return render(
            request,
            self.template_name,
            {"u_form": u_form, "p_form": p_form, "profile": profile},
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
            {"u_form": u_form, "p_form": p_form, "profile": profile},
        )


class UserLoginView(LoginView):
    template_name = "blog/login.html"


class UserLogoutView(LogoutView):
    template_name = "blog/logout.html"
