from django.test import TestCase
from django.urls import reverse, resolve

from checkout.views import (
    cache_checkout_data,
    checkout, checkout_success
)


class TestCheckoutUrls(TestCase):
    """
    Test for Urls for checkout app
    """

    def test_cache_checkout_data_url(self):
        """
        Test for Url for cache checkout data
        before submit form
        """
        url = reverse('cache_checkout_data')
        self.assertEqual(resolve(url).func, cache_checkout_data)

    def test_checkout_url(self):
        """
        Test for Url for checkout
        """
        url = reverse('checkout')
        self.assertEqual(resolve(url).func, checkout)

    def test_checkout_success_url(self):
        """
        Test for Url for checkout success
        """
        url = reverse('checkout_success', kwargs={'order_number': '1'})
        self.assertEqual(resolve(url).func, checkout_success)
