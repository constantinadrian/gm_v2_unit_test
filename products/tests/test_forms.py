from django.test import TestCase

from products.models import Category
from products.forms import ProductForm


class TestProductsModels(TestCase):
    """
    Test for Add Product form
    """

    def setUp(self):
        self.category = Category.objects.create(
            parent=None,
            name="test_category",
            slug="test-category",
            friendly_name="Test Category"
        )
        self.category_parent = Category.objects.create(
            parent=None,
            name="test_category_parent",
            slug="test-category-parent",
            friendly_name="Test Category Parent"
        )
        self.category_child = Category.objects.create(
            parent=self.category_parent,
            name="test_category_child",
            slug="test-category-child",
            friendly_name="Test Category Child"
        )

    def test_product_form_invalid_data(self):
        """
        Test form Add Product with invalid data
        """
        form = ProductForm({
            "sku": "1",
            "brand": "",
            "name": "",
            "slug": "",
            "description": "Test description",
            "price": 14.99,
            "category": self.category,
            "image_url": "",
            "image": "",
            "has_sizes": False,
            "fields_size": 0
        })

        self.assertFalse(form.is_valid())
        self.assertIn("brand", form.errors.keys())
        self.assertEqual(form.errors["brand"][0], "This field is required.")
        self.assertIn("name", form.errors.keys())
        self.assertEqual(form.errors["name"][0], "This field is required.")
        self.assertIn("slug", form.errors.keys())
        self.assertEqual(form.errors["slug"][0], "This field is required.")

    def test_product_form_valid_data(self):
        """
        Test form Add Product with valid data
        """
        form = ProductForm({
            "sku": "1",
            "brand": "Test",
            "name": "Test Product",
            "slug": "test-product",
            "description": "Test description",
            "price": 14.99,
            "category": self.category,
            "image_url": "",
            "image": "",
            "has_sizes": False,
            "fields_size": 0
        })

        self.assertTrue(form.is_valid())
