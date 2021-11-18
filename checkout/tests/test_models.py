from django.test import TestCase, Client
from django.contrib.auth.models import User

from checkout.models import Order, OrderLineItem
from products.models import Category, Product
from profiles.models import UserProfile


class TestCheckoutModels(TestCase):
    """
    Test for checkout models
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
            has_sizes=True,
            fields_size=1
        )
        self.order = Order.objects.create(
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
            delivery_cost='0',
            order_total='14.99',
            grand_total='34.99',
            original_bag={self.product.pk: '1'},
            stripe_pid='123Abc_secret_1abC'
        )
        self.order_line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            product_size='32',
            jacket_size='',
            waistcoat_size='',
            trouser_size='',
            quantity=1,
        )

    def test_order_model(self):
        """
        Test for order model
        """
        order = Order.objects.get(pk=self.order.pk)
        self.assertEqual(str(order), self.order.order_number)

    def test_order_line_item_model(self):
        """
        Test for order line item model
        """
        order_line_item = OrderLineItem.objects.get(
            pk=self.order_line_item.pk)
        self.assertEqual(
            str(order_line_item),
            f'SKU {self.product.sku} on order {self.order.order_number}')
