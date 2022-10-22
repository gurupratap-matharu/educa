from django.db import IntegrityError
from django.test import TestCase

from courses.factories import CourseFactory, SubjectFactory
from courses.models import Course, Subject
from users.factories import StaffuserFactory, UserFactory


class SubjectModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_string_representation(self):
        subject = SubjectFactory()

        self.assertEqual(str(subject), subject.title)

    def test_get_absolute_url(self):
        subject = SubjectFactory()
        expected_url = f"/subjects/{subject.slug.lower()}"

        self.assertEqual(subject.get_absolute_url(), expected_url)

    def test_verbose_name_plural(self):
        subject = SubjectFactory()

        self.assertEqual(str(subject._meta.verbose_name_plural), "subjects")

    def test_subject_model_creation_is_correct(self):
        self.assertEqual(Subject.objects.count(), 0)

        subject = SubjectFactory()
        subject_from_db = Subject.objects.first()

        self.assertEqual(Subject.objects.count(), 1)
        self.assertEqual(subject_from_db.title, subject.title)
        self.assertEqual(subject_from_db.slug, subject.slug)

    def test_subject_title_max_length(self):
        _ = SubjectFactory()
        subject = Subject.objects.first()
        max_length = subject._meta.get_field("title").max_length

        self.assertEqual(max_length, 200)

    def test_subject_slug_max_length(self):
        _ = SubjectFactory()
        subject = Subject.objects.first()
        max_length = subject._meta.get_field("slug").max_length

        self.assertEqual(max_length, 200)

    def test_all_subjects_have_unique_slugs(self):
        _ = Subject.objects.create(title="Music", slug="music")

        with self.assertRaises(IntegrityError):
            Subject.objects.create(title="Music Theory", slug="music")

    def test_all_subjects_are_ordered_correctly(self):
        s_1 = Subject.objects.create(title="Travel", slug="travel")
        s_2 = Subject.objects.create(title="Music", slug="music")
        s_3 = Subject.objects.create(title="Food", slug="food")

        subjects = Subject.objects.all()

        self.assertEqual(subjects[0], s_3)
        self.assertEqual(subjects[1], s_2)
        self.assertEqual(subjects[2], s_1)

        subject = subjects[0]
        ordering = subject._meta.ordering

        self.assertEqual(ordering[0], "title")


class CourseModelTests(TestCase):
    def setUp(self):
        self.owner = StaffuserFactory()
        self.students = UserFactory.create_batch(size=5)
        self.subject = SubjectFactory()
        self.course = CourseFactory(
            subject=self.subject, students=self.students, owner=self.owner
        )

    def test_string_representation(self):
        self.assertEqual(str(self.course), self.course.title)

    def test_get_absolute_url(self):
        slug = self.course.slug.lower()
        expected_url = f"/courses/{slug}/"

        self.assertEqual(self.course.get_absolute_url(), expected_url)

    def test_verbose_name_plural(self):
        self.assertEqual(str(self.course._meta.verbose_name_plural), "courses")

    def test_course_model_creation_is_correct(self):
        course_from_db = Course.objects.first()

        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(course_from_db.title, self.course.title)
        self.assertEqual(course_from_db.slug, self.course.slug)
        self.assertEqual(course_from_db.overview, self.course.overview)
        self.assertEqual(course_from_db.owner, self.course.owner)
        self.assertEqual(course_from_db.subject, self.course.subject)
