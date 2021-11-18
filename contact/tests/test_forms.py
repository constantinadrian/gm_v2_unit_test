from django.test import TestCase

from contact.forms import ContactForm


class TestConatctForms(TestCase):
    """
    Test for Contact forms
    """

    def test_contact_form_invalid_data(self):
        """
        Test contact form with invalid data
        """
        form = ContactForm({
            'name': '',
            'email': '',
            'subject': '',
            'message': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors.keys())
        self.assertEqual(form.errors["name"][0], "This field is required.")
        self.assertIn("email", form.errors.keys())
        self.assertEqual(form.errors["email"][0], "This field is required.")
        self.assertIn("subject", form.errors.keys())
        self.assertEqual(form.errors["subject"][0], "This field is required.")
        self.assertIn("message", form.errors.keys())
        self.assertEqual(form.errors["message"][0], "This field is required.")

    def test_contact_form_valid_data(self):
        """
        Test contact form with valid data
        """
        email = 'test.test@example.com'
        form = ContactForm({
            'name': 'John Doe',
            'email': email,
            'subject': 'Subject',
            'message': 'Message',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean_email(), email)
