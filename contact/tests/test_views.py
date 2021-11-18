from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User


class TestContactViews(TestCase):
    """
    Test for contact views
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            email='test.user@email.com',
            password='testuserpassword'
        )
        self.contact = reverse('contact')

    def test_contact_view_get(self):
        """
        Test for contact view get method
        """
        response = self.client.get(self.contact)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_contact_view_post_invalid_data(self):
        """
        Test for contact view post method with invalid data
        """
        response = self.client.post(
            self.contact,
            data={
                'name': '',
                'email': '',
                'subject': '',
                'message': ''
            })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Failed to send your message. '
            'Please ensure the form is valid.'
            )

    def test_contact_view_post_valid_data_anonymous_user(self):
        """
        Test for contact view post method with valid data
        with anonymous user
        """
        response = self.client.post(
            self.contact,
            data={
                'name': 'Test',
                'email': 'test.user@email.com',
                'subject': 'Subject',
                'message': 'Message'
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.contact)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Your message has been received. '
            'Thank you'
            )

    def test_contact_view_post_valid_data_auth_user(self):
        """
        Test for contact view post method with valid data
        with auth user
        """
        self.assertTrue(self.client.login(
            username="test_user", password="testuserpassword")
        )
        response = self.client.post(
            self.contact,
            data={
                'name': 'Test',
                'email': 'test.user@email.com',
                'subject': 'Subject',
                'message': 'Message'
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.contact)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Your message has been received. '
            'Thank you'
            )
