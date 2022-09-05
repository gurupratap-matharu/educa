# Generated by Django 4.1 on 2022-09-05 15:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("courses", "0004_alter_content_options_alter_module_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="students",
            field=models.ManyToManyField(
                blank=True, related_name="courses_joined", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
