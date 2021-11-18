from django.test import TestCase
from django.urls import reverse, resolve

from products.views import (
    all_products, product_detail,
    add_product, edit_product,
    delete_product
)


class TestUrls(TestCase):
    """
    Test for Urls for products app
    """

    def test_all_products_urls(self):
        """
        Test for Url for all products
        """
        url = reverse('products')
        self.assertEqual(resolve(url).func, all_products)

    def test_all_products_from_category_urls(self):
        """
        Test for Url for all products within a category
        """
        url = reverse(
            'products_from_category',
            kwargs={'category_slug': 'category'})
        self.assertEqual(resolve(url).func, all_products)

    def test_product_detail_urls(self):
        """
        Test for Url for product detail
        """
        url = reverse('product_detail',
                      kwargs={'category_slug': 'category',
                              'product_slug': 'product'})
        self.assertEqual(resolve(url).func, product_detail)

    def test_add_product_urls(self):
        """
        Test for Url for add product
        """
        url = reverse('add_product')
        self.assertEqual(resolve(url).func, add_product)

    def test_edit_product_urls(self):
        """
        Test for Url for edit product detail
        """
        url = reverse('edit_product',
                      kwargs={'product_id': '1'})
        self.assertEqual(resolve(url).func, edit_product)

    def test_delete_product_urls(self):
        """
        Test for Url for delete product detail
        """
        url = reverse('delete_product',
                      kwargs={'product_id': '1'})
        self.assertEqual(resolve(url).func, delete_product)
