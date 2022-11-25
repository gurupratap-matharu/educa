from django.urls import path

from . import views

app_name = "users"


urlpatterns = [
    path("signup/", views.SignupPageView.as_view(), name="signup"),
    path("", views.GeneralView.as_view(), name="general"),
    path("<slug:username>/", views.ProfileView.as_view(), name="profile"),
]
