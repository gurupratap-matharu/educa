from django.db import IntegrityError
from django.test import TestCase

from courses.factories import SubjectFactory
from courses.models import Subject


class SubjectModelTests(TestCase):
    def test_string_representation(self):
        subject = SubjectFactory()
        self.assertEqual(str(subject), subject.title)

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

        self.assertLessEqual(len(subject.title), 200)
        self.assertLessEqual(len(subject.slug), 200)

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
    pass
