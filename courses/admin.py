from typing import Sequence

from django.contrib import admin
from embed_video.admin import AdminVideoMixin

from .models import Content, Course, File, Image, Module, Subject, Text, Video

admin.site.empty_value_display = "(None)"


class ModuleInline(admin.TabularInline):
    model = Module


class ContentInline(admin.StackedInline):
    model = Content


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display: Sequence[str] = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display: Sequence[str] = ["title", "subject", "created"]
    list_filter: Sequence[str] = ["created", "subject"]
    search_fields: Sequence[str] = ["title", "overview"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display: Sequence[str] = ["title", "description", "order", "course"]
    list_filter: Sequence[str] = ["course"]
    search_fields: Sequence[str] = ["title", "description"]
    inlines = [ContentInline]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "order",
        "flavour",
        "module",
    ]

    list_filter = [
        "content_type",
    ]
    list_display_links = ["__str__"]

    @admin.display(description="Name")
    def flavour(self, obj):
        return ("%s" % obj.item._meta.model_name).title()


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display: Sequence[str] = ("title", "snippet", "owner", "created")
    list_filter: Sequence[str] = (
        "created",
        "updated",
    )
    search_fields: Sequence[str] = ["title"]

    def snippet(self, obj):
        data = obj.content
        return (data[:75] + "...") if len(data) > 75 else data


@admin.register(Video)
class VideoAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display: Sequence[str] = ("title", "render", "owner", "created")
    list_filter: Sequence[str] = (
        "created",
        "updated",
    )
    search_fields: Sequence[str] = ["title"]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display: Sequence[str] = ("title", "image", "render", "owner", "created")
    list_filter: Sequence[str] = ("created", "updated")
    search_fields: Sequence[str] = ["title"]


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("title", "file", "render", "owner", "created")
    list_filter = ("created", "updated")
    search_fields: Sequence[str] = ["title"]
