from django.test import SimpleTestCase

from pages.forms import ContactForm


class ContactFormTests(SimpleTestCase):
    def test_contact_form_is_valid_for_valid_data(self):
        form_data = {
            "name": "Guest User",
            "email": "guestuser@email.com",
            "subject": "Just want to say hi!",
            "message": "Hey I have been thinking about you a lot! Would you like to hang around during the weekend?",
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_is_invalid_for_missing_email_field(self):
        form_data = {
            "name": "Guest User",
            "email": "",
            "subject": "Just want to say hi!",
            "message": "Hey I have been thinking about you a lot! Would you like to hang around during the weekend?",
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_contact_form_is_invalid_for_missing_name_field(self):
        form_data = {
            "name": "",
            "email": "guestuser@email.com",
            "subject": "Just want to say hi!",
            "message": "Hey I have been thinking about you a lot! Would you like to hang around during the weekend?",
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_contact_form_is_invalid_for_empty_subject(self):
        form_data = {
            "name": "Guest user",
            "email": "guestuser@email.com",
            "subject": "",
            "message": "Hey I have been thinking about you a lot! Would you like to hang around during the weekend?",
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_contact_form_is_invalid_for_empty_message(self):
        form_data = {
            "name": "Guest user",
            "email": "guestuser@email.com",
            "subject": "Just want to say hi!",
            "message": "",
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
