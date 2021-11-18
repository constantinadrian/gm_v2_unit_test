from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

from products.models import Category, Product


class TestWishlistViews(TestCase):
    """
    Test for wishlist view, add and
    remove from wishlist view
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            email='test.user@email.com',
            password='testuserpassword'
        )
        self.category = Category.objects.create(
            parent=None,
            name="test_category",
            slug="test-category",
            friendly_name="Test Category"
        )
        self.product = Product.objects.create(
            sku="1",
            brand="Test",
            name="Test Product",
            slug="test-product",
            description="Test description",
            price=14.99,
            category=self.category,
            image_url="",
            image="",
            has_sizes=False,
            fields_size=0
        )
        self.wishlist = reverse(
            "wishlist"
        )
        self.add_to_wishlist = reverse(
            "add_to_wishlist",
            kwargs={"product_id": self.product.pk}
        )
        self.account_login = reverse('account_login')

    def test_wishlist_view(self):
        """
        Test for wishlist view
        """
        response = self.client.get(self.wishlist)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wishlist/wishlist.html")
        self.assertTemplateUsed(response, "base.html")

    def test_add_to_wishlist_view_post_for_anonymous_user(self):
        """
        Test for add to wishlist view for AnonymousUser
        """
        response = self.client.post(self.add_to_wishlist)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'{self.account_login}?next=/wishlist/add/1/'
        )

    def test_add_to_wishlist_view_post_for_user(self):
        """
        Test for add to wishlist view for User post method
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        response = self.client.post(self.add_to_wishlist)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         f'{self.product.name} has been '
                         'added to your wishlist.')

    def test_remove_from_wishlist_for_user(self):
        """
        Test for add to wishlist view for User for remove product
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        self.client.post(self.add_to_wishlist)
        response = self.client.post(self.add_to_wishlist)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]),
                         f'{self.product.name} has been '
                         'remove to your wishlist.')

    def test_wishlist_view_empty_page(self):
        """
        Test for wishlist view page is out of range
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        response = self.client.post(self.add_to_wishlist)
        response = self.client.get(self.wishlist,
                                   {"page": "99"})
        self.assertEqual(response.context['wishlist'].number, 1)
