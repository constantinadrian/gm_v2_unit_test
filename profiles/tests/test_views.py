from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

from checkout.models import Order
from profiles.models import UserProfile
from profiles.forms import UserProfileForm


class TestProfilesViews(TestCase):
    """
    Test for Profile views
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            email='test.user@email.com',
            password='testuserpassword'
        )
        self.user_profile_form = UserProfileForm
        self.profile = reverse('profile')
        self.account_login = reverse('account_login')

    def test_profile_view_get_anonymous_user(self):
        """
        Test for profile view get method with anonymous user
        """
        response = self.client.get(self.profile)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'{self.account_login}?next=/profile/'
        )

    def test_profile_view_get_auth_user(self):
        """
        Test for profile view get method with auth user
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        response = self.client.get(self.profile)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile.html")
        self.assertTemplateUsed(response, "base.html")

    def test_profile_view_post_valid_data(self):
        """
        Test for profile view with valid data
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        data = {
            'default_phone_number': '456321',
            'default_street_address1': '123 st',
            'default_street_address2': 'main road',
            'default_town_or_city': 'city',
            'default_county': 'county',
            'default_postcode': '1234',
            'default_country': 'CA'
        }
        response = self.client.post(self.profile, data)
        self.assertEqual(response.status_code, 200)

        form = self.user_profile_form(data, instance=self.user)
        self.assertTrue(form.is_valid())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Profile updated successfully')

    def test_profile_view_post_invalid_data(self):
        """
        Test for profile view with invalid data
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        data = {
            'default_phone_number': '4563219903827365418295',
            'default_street_address1': '',
            'default_street_address2': '',
            'default_town_or_city': '',
            'default_county': '',
            'default_postcode': '',
            'default_country': ''
        }
        response = self.client.post(self.profile, data)
        self.assertEqual(response.status_code, 200)

        form = self.user_profile_form(data, instance=self.user)
        self.assertFalse(form.is_valid())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Update failed. Please ensure the form is valid.')

    def test_order_history_view_get_anonymous_user(self):
        """
        Test for order history get method with anonymous_user
        """

        order = Order.objects.create(user_profile=UserProfile(self.user.pk))
        response = self.client.get(reverse(
            'order_history',
            kwargs={'order_number': order.order_number}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'{self.account_login}?next=/profile/'
            f'order_history/{order.order_number}'
        )

    def test_order_history_view_get_auth_user(self):
        """
        Test for order history get method with auth user
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        order = Order.objects.create(user_profile=UserProfile(self.user.pk))
        response = self.client.get(reverse(
            'order_history',
            kwargs={'order_number': order.order_number}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout_success.html")
        self.assertTemplateUsed(response, "base.html")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'This is a past confirmation for order number '
            f'{order.order_number}. '
            'A confirmation email was sent on the order date.'
        )
