from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class TermsPageView(TemplateView):
    template_name: str = "pages/terms.html"
