from django.test import TestCase
from django.contrib.auth.models import User

from profiles.forms import UserProfileForm


class TestProfilesForms(TestCase):
    """
    Test Profiles forms
    """

    def setUp(self):
        self.user = User.objects.create(
            username='test_user',
            email='test.user@email.com',
            password='testuserpassword'
        )

    def test_user_profile_form_fields_not_required(self):
        """
        Test Profile empty form
        """
        form = UserProfileForm({})
        self.assertTrue(form.is_valid())

    def test_user_profile_form_valid_data(self):
        """
        Test Profile form with valid data
        """
        form = UserProfileForm({
            'user': self.user,
            'default_phone_number': '456321',
            'default_street_address1': '123 st',
            'default_street_address2': 'main road',
            'default_town_or_city': 'city',
            'default_county': 'county',
            'default_postcode': '1234',
            'default_country': 'CA'
        })
        self.assertTrue(form.is_valid())

    def test_user_profile_form_invalid_data(self):
        """
        Test Profile form with invalid data
        """
        form = UserProfileForm({
            'user': self.user,
            'default_phone_number': '4563219903827365418295',
            'default_street_address1': '123 st',
            'default_street_address2': 'main road',
            'default_town_or_city': 'city',
            'default_county': 'county',
            'default_postcode': '1234',
            'default_country': 'CA'
        })
        self.assertFalse(form.is_valid())
        self.assertIn("default_phone_number", form.errors.keys())
        self.assertEqual(
            form.errors["default_phone_number"][0],
            'Ensure this value has at most 20 characters (it has 22).'
        )
