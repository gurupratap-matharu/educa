from rest_framework import serializers

from ..models import Content, Course, Module, Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "title", "slug")


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ("order",)


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ("order", "title", "description", "contents")


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "subject",
            "title",
            "slug",
            "overview",
            "created",
            "owner",
            "modules",
        )
