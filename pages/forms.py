import logging

from django import forms
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, min_length=3, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, min_length=3)
    message = forms.CharField(
        min_length=20,
        max_length=600,
        required=True,
        widget=forms.Textarea(attrs={"cols": 80, "rows": 5}),
    )

    def send_mail(self):

        subject = self.cleaned_data["subject"]
        message = "From: {name}\nEmail: {email}\n\n{message}".format(
            **self.cleaned_data
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=self.cleaned_data["email"],
            recipient_list=[settings.DEFAULT_TO_EMAIL],
            fail_silently=False,
        )
