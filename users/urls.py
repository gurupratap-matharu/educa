from django.urls import path

app_name = "users"


from . import views

urlpatterns = [
    path("signup/", views.SignupPageView.as_view(), name="signup"),
]
