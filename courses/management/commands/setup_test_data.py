"""A utility script to load test data into the db for courses app"""


import random

import factory
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from courses.factories import (
    SUBJECTS,
    CourseFactory,
    FileContentFactory,
    ImageContentFactory,
    ModuleFactory,
    SubjectFactory,
    TextContentFactory,
    VideoContentFactory,
)
from courses.models import Content, Course, File, Image, Module, Text, Video

NUM_SUPERUSERS = 1
NUM_STAFFUSERS = 5
NUM_USERS = 50

NUM_COURSES = 10
NUM_USERS_PER_COURSE = 8
NUM_MODULES_PER_COURSE = 7
NUM_CONTENT_PER_MODULE = 5

CONTENT_FACTORIES = [
    TextContentFactory,
    ImageContentFactory,
    FileContentFactory,
    VideoContentFactory,
]


User = get_user_model()


class Command(BaseCommand):
    """
    Management command which cleans and populates database with mock data
    """

    help = "Loads fake data into the database"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "-l",
            "--locale",
            type=str,
            help="Define a locale for the data to be generated.",
        )

    def success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def danger(self, msg):
        self.stdout.write(self.style.HTTP_BAD_REQUEST(msg))

    def handle(self, *args, **kwargs):
        locale = kwargs.get("locale")

        self.success("Locale: %s" % locale)
        self.danger("Deleting old data...")

        models = [Course, Module, Content, Text, Image, Video, File]
        for m in models:
            m.objects.all().delete()

        self.success("Creating new data...")

        users = User.objects.all()
        superuser = User.objects.get(email__icontains="gurupratap")

        students = random.choices(users, k=NUM_USERS_PER_COURSE)
        students.append(superuser)

        with factory.Faker.override_default_locale(locale):
            courses = CourseFactory.create_batch(size=NUM_COURSES, students=students)

            for course in courses:

                modules = ModuleFactory.create_batch(
                    size=NUM_MODULES_PER_COURSE, course=course
                )

                for m in modules:
                    TextContentFactory(module=m)
                    ImageContentFactory(module=m)
                    VideoContentFactory(module=m)
                    FileContentFactory(module=m)

        all_users = User.objects.count()
        all_staff = User.objects.filter(is_staff=True).count()
        all_courses = Course.objects.count()
        all_modules = Module.objects.count()

        self.success(
            f"""
        Users  : {all_users}
        Staff  : {all_staff}
        Courses: {all_courses}
        Modules: {all_modules}
        """
        )

        self.success("All done! 💖💅🏻💫")
