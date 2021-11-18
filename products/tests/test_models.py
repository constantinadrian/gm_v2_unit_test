from django.test import TestCase

from products.models import Category, Product


class TestProductsModels(TestCase):
    """
    Test for Category and Product models
    """

    def setUp(self):
        self.category = Category.objects.create(
            parent=None,
            name="test_category",
            slug="",
            friendly_name="Test Category"
        )

        self.product = Product.objects.create(
            sku="1",
            brand="Test",
            name="Test Product",
            slug="",
            description="Test description",
            price=14.99,
            category=self.category,
            image_url="",
            image="",
            has_sizes=False,
            fields_size=0
        )

    def test_category_model(self):
        """
        Test for category model
        """
        category = Category.objects.get(pk=self.category.pk)
        self.assertEqual(str(category), self.category.name)

    def test_product_model(self):
        """
        Test for product model
        """
        product = Product.objects.get(pk=self.product.pk)
        self.assertEqual(str(product), self.product.name)
