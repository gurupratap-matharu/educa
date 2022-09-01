from django.forms.models import inlineformset_factory

from .models import Course, Module

ModuleFormSet = inlineformset_factory(
    parent_model=Course,
    model=Module,
    fields=["title", "description"],
    extra=2,
    can_delete=True,
)
