from django.test import TestCase
from django.urls import resolve, reverse

from users import views


class SignupPageTests(TestCase):
    def setUp(self):
        url = reverse("users:signup")
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertContains(self.response, "Signup")
        self.assertNotContains(self.response, "Hi I should not be on this page!")

    def test_signuppage_view_resolves_to_correct_view(self):
        view = resolve("/accounts/signup/")
        actual_view = view.func.__name__
        expected_view = views.SignupPageView.as_view().__name__

        self.assertEqual(actual_view, expected_view)
