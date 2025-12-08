from django.urls import path
from .views import RegisterView, ProfileView, UserLoginView, UserLogoutView

app_name = "blog"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
