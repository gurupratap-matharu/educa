from django.test import SimpleTestCase
from django.urls import resolve, reverse

from pages.views import AboutPageView, HomePageView, TermsPageView


class HomePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("pages:home")
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "pages/home.html")

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, "Home")

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on this page.")

    def test_homepage_url_resolves_homepageview(self):
        view = resolve(reverse("pages:home"))
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class AboutPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("pages:about")
        self.response = self.client.get(url)

    def test_aboutpage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_aboutpage_renders_correct_template(self):
        self.assertTemplateUsed(self.response, "pages/about.html")

    def test_aboutpage_contains_correct_html(self):
        self.assertContains(self.response, "About")

    def test_aboutpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on this page.")

    def test_aboutpage_url_resolves_aboutpageview(self):
        view = resolve(reverse("pages:about"))
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)


class TermsPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("pages:terms")
        self.response = self.client.get(url)

    def test_termspage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_termspage_renders_correct_template(self):
        self.assertTemplateUsed(self.response, "pages/terms.html")

    def test_termspage_contains_correct_html(self):
        self.assertContains(self.response, "Terms")

    def test_termspage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi I should not be on this page!")

    def test_termspage_url_resolves_termspageview(self):
        view = resolve(reverse("pages:terms"))
        self.assertEqual(view.func.__name__, TermsPageView.as_view().__name__)
