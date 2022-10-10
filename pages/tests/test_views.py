from http import HTTPStatus

from django.test import SimpleTestCase
from django.urls import resolve, reverse

from pages.forms import ContactForm
from pages.views import (
    AboutPageView,
    ContactPageView,
    HomePageView,
    PrivacyPageView,
    TermsPageView,
)


class HomePageTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("pages:home")
        self.response = self.client.get(self.url)
        self.template_name = "pages/home.html"

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, self.template_name)

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, "Home")

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on this page.")

    def test_homepage_url_resolves_homepageview(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class AboutPageTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("pages:about")
        self.response = self.client.get(self.url)
        self.template_name = "pages/about.html"

    def test_aboutpage_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_aboutpage_renders_correct_template(self):
        self.assertTemplateUsed(self.response, self.template_name)

    def test_aboutpage_contains_correct_html(self):
        self.assertContains(self.response, "About")

    def test_aboutpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on this page.")

    def test_aboutpage_url_resolves_aboutpageview(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)


class TermsPageTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("pages:terms")
        self.response = self.client.get(self.url)
        self.template_name = "pages/terms.html"

    def test_termspage_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_termspage_renders_correct_template(self):
        self.assertTemplateUsed(self.response, self.template_name)

    def test_termspage_contains_correct_html(self):
        self.assertContains(self.response, "Terms")

    def test_termspage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi I should not be on this page!")

    def test_termspage_url_resolves_termspageview(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, TermsPageView.as_view().__name__)


class PrivacyPageTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("pages:privacy")
        self.response = self.client.get(self.url)
        self.template_name = "pages/privacy.html"

    def test_privacy_page_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_privacy_page_renders_correct_template(self):
        self.assertTemplateUsed(self.response, self.template_name)

    def test_privacy_page_contains_correct_html(self):
        self.assertContains(self.response, "Privacy")

    def test_privacy_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi I should not be on this page!")

    def test_privacy_page_url_resolves_privacypageview(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, PrivacyPageView.as_view().__name__)


class ContactPageTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("pages:contact")
        self.response = self.client.get(self.url)
        self.field_required_msg = "This field is required."

    def test_contact_page_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_contact_page_renders_correct_template(self):
        self.assertTemplateUsed(self.response, "pages/contact.html")

    def test_contact_page_contains_correct_html(self):
        self.assertContains(self.response, "Contact")

    def test_contact_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi I should not be on this page!")

    def test_contact_page_url_resolves_contactpageview(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, ContactPageView.as_view().__name__)

    def test_contact_page_renders_contactform(self):
        form = self.response.context["form"]
        self.assertIsInstance(form, ContactForm)

    def test_contact_page_with_empty_form_submission_raises_valid_errors(self):
        response = self.client.post(self.url, data={})
        self.assertFormError(response, "form", "name", self.field_required_msg)
        self.assertFormError(response, "form", "email", self.field_required_msg)
        self.assertFormError(response, "form", "subject", self.field_required_msg)
        self.assertFormError(response, "form", "message", self.field_required_msg)

    def test_contact_page_with_invalid_field_lengths_raises_valid_errors(self):
        invalid_data = {
            "name": "ab",
            "email": "a@b.com",
            "subject": "XX",
            "message": "-",
        }
        response = self.client.post(self.url, invalid_data)

        self.assertFormError(
            response,
            "form",
            "name",
            "Ensure this value has at least 3 characters (it has 2).",
        )
        self.assertFormError(
            response,
            "form",
            "email",
            "Ensure this value has at least 10 characters (it has 7).",
        )
        self.assertFormError(
            response,
            "form",
            "subject",
            "Ensure this value has at least 3 characters (it has 2).",
        )
        self.assertFormError(
            response,
            "form",
            "message",
            "Ensure this value has at least 20 characters (it has 1).",
        )
