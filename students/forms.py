from django import forms

from courses.models import Course


class CourseEnrollForm(forms.Form):
    """Form to allow students to enroll into a course."""

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), widget=forms.HiddenInput
    )
