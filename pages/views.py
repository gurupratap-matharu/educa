from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ContactForm


class HomePageView(TemplateView):
    template_name: str = "pages/home.html"


class AboutPageView(TemplateView):
    template_name: str = "pages/about.html"


class TermsPageView(TemplateView):
    template_name: str = "pages/terms.html"


class PrivacyPageView(TemplateView):
    template_name: str = "pages/privacy.html"


class ContactPageView(SuccessMessageMixin, FormView):
    template_name: str = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("pages:home")
    success_message: str = "Message sent successfully 🤞"

    def form_valid(self, form) -> HttpResponse:
        form.send_mail()
        return super().form_valid(form)
