from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string
from embed_video.fields import EmbedVideoField

from .fields import OrderField


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]


def get_sentinel_subject():
    return Subject.objects.get_or_create(title="deleted", slug="deleted")[0]


def get_sentinel_course():
    return Course.objects.get_or_create(
        owner=get_sentinel_user(),
        subject=get_sentinel_subject(),
        title="deleted",
        slug="deleted",
    )[0]


def user_directory_path(instance, filename):
    """
    Generate a custom path for each user where his/her files will be saved
    File will be uploaded to `MEDIA_ROOT/user_<id>/<filename>`
    """

    return "user_{0}/{1}".format(instance.owner.id, filename)


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="courses_created",
        on_delete=models.SET(get_sentinel_user),  # type: ignore
    )
    subject = models.ForeignKey(
        Subject, related_name="courses", on_delete=models.SET(get_sentinel_subject)  # type: ignore
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="courses_joined", blank=True
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=["course"])  # type: ignore

    def __str__(self):
        return f"{self.order}. {self.title}"

    class Meta:
        ordering = ["order"]


class Content(models.Model):
    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ("text", "video", "image", "file")},
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    order = OrderField(blank=True, for_fields=["module"])  # type: ignore

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.item}"

    def render(self):
        return self.item.render()


class ItemBase(models.Model):
    """
    Abstract class which represents a generic (multimedia) content type.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_related",
        on_delete=models.SET(get_sentinel_user),
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(
            f"courses/content/{self._meta.model_name}.html", {"item": self}
        )


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to=user_directory_path)


class Image(ItemBase):
    image = models.ImageField(upload_to=user_directory_path)


class Video(ItemBase):
    url = EmbedVideoField()
