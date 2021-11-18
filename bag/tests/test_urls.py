from django.test import TestCase
from django.urls import reverse, resolve

from bag.views import (
    view_bag, add_to_bag,
    adjust_bag, remove_from_bag
)


class TestBagUrls(TestCase):
    """
    Test for Urls for bag app
    """

    def test_view_bag_url(self):
        """
        Test for Url for view bag
        """
        url = reverse('view_bag')
        self.assertEqual(resolve(url).func, view_bag)

    def test_add_to_bag_url(self):
        """
        Test for Url for add to bag
        """
        url = reverse('add_to_bag', kwargs={'item_id': '1'})
        self.assertEqual(resolve(url).func, add_to_bag)

    def test_adjust_bag_url(self):
        """
        Test for Url for adjust bag
        """
        url = reverse('adjust_bag', kwargs={'item_id': '1'})
        self.assertEqual(resolve(url).func, adjust_bag)

    def test_remove_from_bag_url(self):
        """
        Test for Url for remove from bag
        """
        url = reverse('remove_from_bag', kwargs={'item_id': '1'})
        self.assertEqual(resolve(url).func, remove_from_bag)
