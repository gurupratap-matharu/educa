import pdb
from http import HTTPStatus

from django.test import TestCase
from django.urls import resolve, reverse

from courses.factories import CourseFactory, SubjectFactory
from courses.views import CourseListView
from users.factories import StaffuserFactory, UserFactory


class CourseListViewTests(TestCase):
    """Test suite for testing course list views."""

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.url = reverse("courses:course_list")
        self.template_name = "courses/course_list.html"
        self.response = self.client.get(self.url)

    def test_course_list_url_accessible_by_name(self):
        response = self.client.get(reverse("courses:course_list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_course_list_url_exists_at_desired_location(self):
        response = self.client.get("/courses/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

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

    def test_course_list_view_shows_message_for_no_data(self):
        self.assertContains(self.response, "There are no subjects yet")
        self.assertContains(self.response, "There are no courses yet!")

    def test_course_list_view_shows_all_courses(self):
        subject = SubjectFactory()
        owner = StaffuserFactory()
        students = UserFactory.create_batch(size=3)
        _ = CourseFactory.create_batch(
            size=2, owner=owner, students=students, subject=subject
        )

        response = self.client.get(self.url)

        self.assertEqual(len(response.context["subjects"]), 1)
        self.assertEqual(len(response.context["courses"]), 2)


class CourseDetailViewTests(TestCase):
    pass
