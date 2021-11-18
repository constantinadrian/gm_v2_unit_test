from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

from checkout.models import Order
from profiles.models import UserProfile
from products.models import Category, Product


class TestCheckoutViews(TestCase):
    """
    Test for checkout views
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
        self.product1 = Product.objects.create(
            sku="2",
            brand="Test",
            name="Test Product",
            slug="test-product-1",
            description="Test description",
            price=14.99,
            category=self.category,
            image_url="",
            image="",
            has_sizes=True,
            fields_size=1
        )
        self.product2 = Product.objects.create(
            sku="3",
            brand="Test",
            name="Test Product",
            slug="test-product-2",
            description="Test description",
            price=14.99,
            category=self.category,
            image_url="",
            image="",
            has_sizes=True,
            fields_size=2
        )
        self.product3 = Product.objects.create(
            sku="4",
            brand="Test",
            name="Test Product",
            slug="test-product-3",
            description="Test description",
            price=14.99,
            category=self.category,
            image_url="",
            image="",
            has_sizes=True,
            fields_size=3
        )
        self.add_to_bag = reverse(
            'add_to_bag',
            kwargs={'item_id': self.product.pk})
        self.add_to_bag1 = reverse(
            'add_to_bag',
            kwargs={'item_id': self.product1.pk})
        self.add_to_bag2 = reverse(
            'add_to_bag',
            kwargs={'item_id': self.product2.pk})
        self.add_to_bag3 = reverse(
            'add_to_bag',
            kwargs={'item_id': self.product3.pk})
        self.checkout = reverse('checkout')
        self.cache_checkout_data = reverse('cache_checkout_data')

    def test_checkout_view_get_empty_bag(self):
        """
        Test for checkout view get method with empty bag
        """
        response = self.client.get(self.checkout)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "There's nothing in your  \
                bag at the moment"
            )

    def test_checkout_view_get_with_bag_anonymous_user(self):
        """
        Test for checkout view get method with bag for
        anonymous user
        """
        self.client.post(
            self.add_to_bag,
            data={
                'quantity': '1',
                'redirect_url': '/',
            })
        response = self.client.get(self.checkout)
        self.assertEqual(response.status_code, 200)

    def test_checkout_view_get_with_bag_auth_user(self):
        """
        Test for checkout view get method with bag for
        auth user
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        self.client.post(
            self.add_to_bag,
            data={
                'quantity': '1',
                'redirect_url': '/',
            })
        response = self.client.get(self.checkout)
        self.assertEqual(response.status_code, 200)

    def test_checkout_view_post_with_bag_auth_user_invalid_form(self):
        """
        Test for checkout view post method with bag for
        auth user and invalid checkout form
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        self.client.post(
            self.add_to_bag,
            data={
                'quantity': '1',
                'redirect_url': '/',
            })
        response = self.client.post(
            self.checkout,
            data={
                'full_name': '',
                'email': '',
                'phone_number': '',
                'country': '',
                'postcode': '',
                'town_or_city': '',
                'street_address1': '',
                'street_address2': '',
                'county': '',
                'client_secret': ''
            })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(
            str(messages[1]), 'There was an error with your form. \
                Please double check your information.'
            )

    def test_checkout_post_with_user_valid_form_product_no_size(self):
        """
        Test for checkout view post method with bag for
        auth user and valid checkout form
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        self.client.post(
            self.add_to_bag,
            data={
                'quantity': '1',
                'redirect_url': '/',
            })
        response = self.client.post(
            self.checkout,
            data={
                'full_name': 'John Doe',
                'email': 'test.user@email.com',
                'phone_number': '12345',
                'country': 'IE',
                'postcode': 'D1 123',
                'town_or_city': 'Dublin',
                'street_address1': '12 main st',
                'street_address2': 'second st',
                'county': 'D1',
                'client_secret': 'client'
            })
        self.assertEqual(response.status_code, 302)

    def test_checkout_post_with_user_valid_form_product_one_size(self):
        """
        Test for checkout view post method with bag for
        auth user and valid checkout form for product with one size
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        self.client.post(
            self.add_to_bag1,
            data={
                'quantity': '1',
                'redirect_url': '/',
                'product_size': '32'
            })
        response = self.client.post(
            self.checkout,
            data={
                'full_name': 'John Doe',
                'email': 'test.user@email.com',
                'phone_number': '12345',
                'country': 'IE',
                'postcode': 'D1 123',
                'town_or_city': 'Dublin',
                'street_address1': '12 main st',
                'street_address2': 'second st',
                'county': 'D1',
                'client_secret': '123_secret_456'
            })
        self.assertEqual(response.status_code, 302)

    def test_checkout_post_with_user_valid_form_product_two_size(self):
        """
        Test for checkout view post method with bag for
        auth user and valid checkout form for product with two size
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        self.client.post(
            self.add_to_bag2,
            data={
                'quantity': '1',
                'redirect_url': '/',
                'jacket_size': '32',
                'trouser_size': '32'
            })
        response = self.client.post(
            self.checkout,
            data={
                'full_name': 'John Doe',
                'email': 'test.user@email.com',
                'phone_number': '12345',
                'country': 'IE',
                'postcode': 'D1 123',
                'town_or_city': 'Dublin',
                'street_address1': '12 main st',
                'street_address2': 'second st',
                'county': 'D1',
                'client_secret': '123_secret_456'
            })
        self.assertEqual(response.status_code, 302)

    def test_checkout_post_with_user_valid_form_product_three_size(self):
        """
        Test for checkout view post method with bag for
        auth user and valid checkout form for product with three size
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        self.client.post(
            self.add_to_bag3,
            data={
                'quantity': '1',
                'redirect_url': '/',
                'jacket_size': '32',
                'waistcoat_size': '32',
                'trouser_size': '32'
            })
        response = self.client.post(
            self.checkout,
            data={
                'full_name': 'John Doe',
                'email': 'test.user@email.com',
                'phone_number': '12345',
                'country': 'IE',
                'postcode': 'D1 123',
                'town_or_city': 'Dublin',
                'street_address1': '12 main st',
                'street_address2': 'second st',
                'county': 'D1',
                'client_secret': '123_secret_456'
            })
        self.assertEqual(response.status_code, 302)

    def test_cache_checkout_data_400(self):
        """
        Test view that cache data when the checkout
        form is submitted returning 400 status code
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        response = self.client.post(
            self.cache_checkout_data,
            data={
                'client_secret': '123Abc_secret_1abC',
                'save_info': False
            })
        self.assertEqual(response.status_code, 400)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Sorry, your payment cannot be \
            processed right now. Please try again later.'
        )

    def test_checkout_success(self):
        """
        Test view that cache data when the checkout form is submitted
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        bag = {'1': 1}
        session = self.client.session
        session['bag'] = bag
        session['save_info'] = True
        session.save()

        order = Order.objects.create(
            order_number='123',
            user_profile=UserProfile(self.user.pk),
            full_name='testuser',
            email='test.user@email.com',
            phone_number='123456',
            country='IE',
            postcode='D1 123',
            town_or_city='Dublin',
            street_address1='133 main st',
            street_address2='',
            county='',
            delivery_cost='20',
            order_total='40',
            grand_total='40',
            original_bag=bag,
            stripe_pid='123Abc_secret_1abC'
        )

        response = self.client.post(
            reverse('checkout_success',
                    kwargs={'order_number': order.order_number})
        )
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Order successfully processed! '
            f'Your order number is {order.order_number}. A confirmation '
            f'email will be sent to {order.email}.'
        )
