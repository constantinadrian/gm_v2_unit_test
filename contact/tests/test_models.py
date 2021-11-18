from django.test import TestCase, Client
from django.contrib.auth.models import User

from contact.models import Contact
from profiles.models import UserProfile


class TestContactModels(TestCase):
    """
    Test for contact models
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            email='test.user@email.com',
            password='testuserpassword'
        )
        self.contact_message = Contact.objects.create(
            user_profile=UserProfile(self.user.pk),
            name='John Doe',
            email='test.user@email.com',
            subject='Subject',
            message='Message'
        )

    def test_contact_model(self):
        """
        Test for Contact model str
        """
        contact_message = Contact.objects.get(
            user_profile=UserProfile(self.user.pk),
            subject=self.contact_message.subject
        )
        self.assertEqual(
            str(contact_message),
            f"{self.contact_message.name}"
            )
