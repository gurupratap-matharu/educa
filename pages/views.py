from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name: str = "pages/home.html"


class AboutPageView(TemplateView):
    template_name: str = "pages/about.html"


class TermsPageView(TemplateView):
    template_name: str = "pages/terms.html"


class PrivacyPageView(TemplateView):
    template_name: str = "pages/privacy.html"
