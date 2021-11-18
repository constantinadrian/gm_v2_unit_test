from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages

from newsletter.models import Newsletter


class TestNewsletterSignupViews(TestCase):
    """
    Test for Newsletter Signup view
    """

    def setUp(self):
        self.client = Client()
        self.newsletter_signup = reverse('newsletter_signup')
        self.redirect_url = reverse('home')

    def test_newsletter_signup_view_post_invalid_data(self):
        """
        Test Newsletter Signup view with post method
        with invalid data
        """
        response = self.client.post(
            self.newsletter_signup,
            data={
                'email': '',
                'redirect_url': self.redirect_url
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Please ensure the email '
                         'address on the form is valid.')

    def test_newsletter_signup_view_post_valid_data(self):
        """
        Test Newsletter Signup view with post method
        with valid data
        """
        email = 'test.test@example.com'
        response = self.client.post(
            self.newsletter_signup,
            data={
                'email': email,
                'redirect_url': self.redirect_url
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         f'Thank you. You are now subscribed '
                         f'to our newsletter. A confirmation '
                         f'email will be sent to {email}.')

    def test_newsletter_signup_view_post_existing_email(self):
        """
        Test Newsletter Signup view with post method
        with valid data
        """
        email = 'test.test@example.com'
        Newsletter.objects.create(email=email)

        response = self.client.post(
            self.newsletter_signup,
            data={
                'email': email,
                'redirect_url': self.redirect_url
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'This email address is already '
                         'subscribed to our newsletter.')
