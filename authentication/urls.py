from django.urls import path

# generic view :
# - LoginView
# - LogoutView
# - PasswordChangeView
# - PasswordChangeDoneView
# - PasswordResetView
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
from authentication.views import signup, profile, profile_update

urlpatterns = [
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
    path("profile/", profile, name="profile"),
    path("profile/profile_update", profile_update, name="profile_update"),
]
