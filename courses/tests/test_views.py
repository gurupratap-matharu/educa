from http import HTTPStatus

from django.test import TestCase
from django.urls import resolve, reverse

from courses.views import CourseListView


class CourseListViewTests(TestCase):
    """Test suite for testing course list views."""

    def setUp(self):
        self.url = reverse("courses:course_list")
        self.template_name = "courses/course_list.html"
        self.response = self.client.get(self.url)

    def test_course_list_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_course_list_renders_correct_template(self):
        self.assertTemplateUsed(self.response, self.template_name)

    def test_course_list_contains_correct_html(self):
        self.assertContains(self.response, "courses")

    def test_course_list_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi I should not be on this page")

    def test_course_list_url_resolves_courselistview(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, CourseListView.as_view().__name__)


class CourseDetailViewTests(TestCase):
    pass
