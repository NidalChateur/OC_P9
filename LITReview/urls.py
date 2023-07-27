"""
URL configuration for LITRewiew project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# generic view :  LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,PasswordResetView
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from review.views import home, ticket_create, review_create
from authentication.views import signup

urlpatterns = [
    path("admin/", admin.site.urls),
    # redirect_authenticated_user=True redirect the user to the homepage after connexion
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("signup/", signup, name="signup"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path(
        "password_change/",
        PasswordChangeView.as_view(template_name="authentication/password_change.html"),
        name="password_change",
    ),
    path(
        "password_change_done/",
        PasswordChangeDoneView.as_view(
            template_name="authentication/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="authentication/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(
            template_name="authentication/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="authentication/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="authentication/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("home/", home, name="home"),
    path("home/add_ticket/", ticket_create, name="ticket-create"),
    path("home/add_review/", review_create, name="review-create"),
]
