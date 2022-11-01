from django.urls import path

from . import views

app_name = "pages"


urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("terms/", views.TermsPageView.as_view(), name="terms"),
    path("privacy/", views.PrivacyPageView.as_view(), name="privacy"),
    path("contact/", views.ContactPageView.as_view(), name="contact"),
    path(
        "base-fullscreen/",
        views.BaseFullscreenPageView.as_view(),
        name="base-fullscreen",
    ),
    path("favicon.ico", views.favicon),
]
