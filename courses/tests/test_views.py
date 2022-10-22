from http import HTTPStatus

from django.test import TestCase
from django.urls import resolve, reverse

from courses.factories import CourseFactory, ModuleFactory, SubjectFactory
from courses.models import Course, Subject
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


class CourseListSubjectViewTests(TestCase):
    """
    Test suite for Course list filtered by a subject

    This uses as the same view as CourseListView but has a different url endpoint called `course_list_subject` which takes the subject-slug as a parameter.
    """

    def setUp(self):
        self.owner = StaffuserFactory()
        self.students = UserFactory.create_batch(size=5)

        self.subject = SubjectFactory()  # Selected in our view
        self.subject_deselected = SubjectFactory()  # Not selected in our view

        self.courses = CourseFactory.create_batch(
            size=3,
            subject=self.subject,
            students=self.students,
            owner=self.owner,
        )  # Selected in our view

        self.courses_deselected = CourseFactory.create_batch(
            size=3,
            subject=self.subject_deselected,
            students=self.students,
            owner=self.owner,
        )  # Not selected in our view

        for course in self.courses:
            ModuleFactory.create_batch(size=2, course=course)

        self.template_name = "courses/course_list.html"
        self.url = reverse("courses:course_list_subject", args=[self.subject.slug])
        self.response = self.client.get(self.url)

    def test_course_list_subject_url_accessible_by_name(self):
        response = self.client.get(
            reverse("courses:course_list_subject", args=[self.subject.slug])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_course_list_subject_url_exists_at_desired_location(self):
        response = self.client.get(f"/courses/subject/{self.subject.slug}/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_course_list_subject_status_code(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_course_list_subject_renders_correct_template(self):
        self.assertTemplateUsed(self.response, self.template_name)

    def test_course_list_subject_contains_correct_html(self):
        self.assertContains(self.response, "courses")
        self.assertContains(self.response, str(self.subject))

    def test_course_list_subject_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi I should not be on this page")

    def test_course_list_subject_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, CourseListView.as_view().__name__)

    def test_course_list_subject_view_shows_message_for_no_data(self):
        # Delete all Subject and Course from database which are created in setup() method
        Subject.objects.all().delete()
        Course.objects.all().delete()

        # Fetch course and subject that do not exist
        invalid_subject_url = "/courses/subject/music/"
        response = self.client.get(invalid_subject_url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateNotUsed(response, self.template_name)

    def test_course_list_subject_view_shows_all_courses_for_a_subject(self):
        self.assertEqual(self.response.context["subject"], self.subject)
        self.assertEqual(len(self.response.context["subjects"]), 2)
        # Deselected courses should not be part of context. So count is 3 and not 6
        self.assertEqual(len(self.response.context["courses"]), 3)

    def test_subject_and_course_have_annotated_attributes(self):
        # Veer check if running for loop in a single test is correct or not!
        for s in self.response.context["subjects"]:
            self.assertEqual(s.total_courses, 3)

        for c in self.response.context["courses"]:
            self.assertEqual(c.total_modules, 2)


class CourseDetailViewTests(TestCase):
    pass
