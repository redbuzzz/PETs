from django.contrib.auth.decorators import login_required
from django.urls import path

from web.views import registration_view, login_view, logout_view, homepage_view

urlpatterns = [
    path("registration/", registration_view, name="registration"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", homepage_view, name="homepage"),
]
