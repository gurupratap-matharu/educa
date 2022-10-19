import factory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from faker import Faker

from courses.models import Content, Course, File, Image, Module, Subject, Text, Video

User = get_user_model()
fake = Faker()

SUBJECTS = [
    "Programming",
    "Language Learning",
    "Music",
    "Wood Working",
    "Investing",
    "Fitness",
    "Handwriting",
    "Business",
    "Economics",
    "Dance",
    "Meditation",
    "Writing",
]


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject
        django_get_or_create = ("title",)

    title = factory.Faker("random_element", elements=SUBJECTS)
    slug = factory.LazyAttribute(lambda obj: fake.slug(value=obj.title))


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course
        django_get_or_create = ("title", "slug")

    owner = factory.Iterator(User.objects.filter(is_staff=True))
    subject = factory.SubFactory(SubjectFactory)
    title = factory.Faker("catch_phrase")
    slug = factory.LazyAttribute(lambda obj: fake.slug(value=obj.title))
    overview = factory.Faker("text", max_nb_chars=500)
    created = factory.Faker("date_time_this_decade")

    @factory.post_generation
    def students(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of students were passed in, use them
            for student in extracted:
                self.students.add(student)  # type: ignore


class ModuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Module
        django_get_or_create = ("title",)

    course = factory.SubFactory(CourseFactory)
    title = factory.Faker("bs")
    description = factory.Faker("text", max_nb_chars=500)


class ItemBaseFactory(factory.django.DjangoModelFactory):
    owner = factory.Iterator(User.objects.filter(is_staff=True))
    title = factory.Faker("word")
    created = factory.Faker("date_time_this_decade")

    class Meta:
        abstract = True
        django_get_or_create = ("title",)


class TextFactory(ItemBaseFactory):
    content = factory.Faker("text", max_nb_chars=500)

    class Meta:
        model = Text


class VideoFactory(ItemBaseFactory):
    url = "https://www.youtube.com/watch?v=Yq82CKp_ToM"

    class Meta:
        model = Video


class ImageFactory(ItemBaseFactory):
    image = factory.django.ImageField(color="pink")

    class Meta:
        model = Image


class FileFactory(ItemBaseFactory):
    file = factory.django.FileField(filename="notes.pdf")

    class Meta:
        model = File


class ContentFactory(factory.django.DjangoModelFactory):
    module = factory.SubFactory(ModuleFactory)
    object_id = factory.SelfAttribute("item.id")
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.item)
    )

    class Meta:
        abstract = True
        exclude = ["item"]


class ImageContentFactory(ContentFactory):
    item = factory.SubFactory(ImageFactory)

    class Meta:
        model = Content


class VideoContentFactory(ContentFactory):
    item = factory.SubFactory(VideoFactory)

    class Meta:
        model = Content


class FileContentFactory(ContentFactory):
    item = factory.SubFactory(FileFactory)

    class Meta:
        model = Content


class TextContentFactory(ContentFactory):
    item = factory.SubFactory(TextFactory)

    class Meta:
        model = Content
