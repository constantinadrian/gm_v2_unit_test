from django.test import TestCase, Client
from django.contrib.auth.models import User

from wishlist.models import Wishlist


class TestWishlistModels(TestCase):
    """
    Test for Wishlist models
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test.user@email.com',
            password='testuserpassword'
        )

    def test_category_model(self):
        """
        Test for category model
        """
        wishlist = Wishlist.objects.get(user=self.user)
        self.assertEqual(str(wishlist), self.user.username)
