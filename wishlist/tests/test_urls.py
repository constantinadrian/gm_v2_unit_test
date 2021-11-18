from django.test import TestCase
from django.urls import reverse, resolve

from wishlist.views import wishlist, add_to_wishlist


class TestWishlistUrls(TestCase):
    """
    Test for Urls for Wishlist app
    """

    def test_all_wishlist_url(self):
        """
        Test for all Wishlist url
        """
        url = reverse('wishlist')
        self.assertEqual(resolve(url).func, wishlist)

    def test_add_to_wishlist_url(self):
        """
        Test for add to Wishlist url
        """
        url = reverse('add_to_wishlist', kwargs={'product_id': '1'})
        self.assertEqual(resolve(url).func, add_to_wishlist)
