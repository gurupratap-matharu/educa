from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm


class SignupPageView(CreateView):
    form_class = CustomUserCreationForm

    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class ProfileView(TemplateView):
    template_name = "users/profile.html"
