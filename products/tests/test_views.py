from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

from products.models import Category, Product


class TestProductsViews(TestCase):
    """
    Test for all products, including
    sorting and search queries.
    """

    def setUp(self):
        self.client = Client()
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
        self.product_for_category_child = Product.objects.create(
            sku="2",
            brand="Test",
            name="Test Product Child",
            slug="test-product-child",
            description="Test description child",
            price=4.99,
            category=self.category_child,
            image_url="",
            image="",
            has_sizes=False,
            fields_size=0
        )
        self.all_products = reverse(
            "products"
        )
        self.products_from_category = reverse(
            "products_from_category",
            kwargs={"category_slug": self.category.slug}
        )
        self.products_from_category_parent = reverse(
            "products_from_category",
            kwargs={"category_slug": self.category_parent.slug}
        )
        self.products_from_category_child = reverse(
            "products_from_category",
            kwargs={"category_slug": self.category_child.slug}
        )

    def test_all_products_view(self):
        """
        Test for all Products view
        """
        response = self.client.get(self.all_products)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertTemplateUsed(response, "base.html")

    def test_all_products_within_category_no_parent_child_relation(self):
        """
        Test for all Products view within a category
        that has no parent and is not a parent category
        """
        response = self.client.get(self.products_from_category)
        context = response.context
        category = Category.objects.get(name=self.category.name)
        self.assertTrue(context['current_categories'])
        self.assertEqual(list(context['current_categories']), [category])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertTemplateUsed(response, "base.html")

    def test_all_products_within_category_parent(self):
        """
        Test for all Products view within a parent category
        """
        response = self.client.get(self.products_from_category_parent)
        context = response.context
        category = Category.objects.get(name=self.category_parent.name)
        self.assertTrue(context['current_categories'])
        self.assertEqual(list(context['current_categories']), [category])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertTemplateUsed(response, "base.html")

    def test_all_products_within_category_child(self):
        """
        Test for all Products view within a child category
        """
        response = self.client.get(self.products_from_category_child)
        context = response.context
        category = Category.objects.get(name=self.category_child.name)
        self.assertTrue(context['current_categories'])
        self.assertEqual(list(context['current_categories']), [category])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertTemplateUsed(response, "base.html")

    def test_all_products_view_with_search_query(self):
        """
        Test for all Products view with search query
        """
        response = self.client.get(self.all_products,
                                   {"q": "test"})
        context = response.context
        self.assertTrue(context["search_term"])
        self.assertEqual(context["search_term"], "test")

    def test_all_products_view_with_empty_search_query(self):
        """
        Test for all Products view with empty search query
        """
        response = self.client.get(self.all_products,
                                   {"q": ""})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "You didn't enter any search criteria!")

    def test_all_products_view_with_sort_by_name(self):
        """
        Test for all Products view with sort by name parameter
        """
        response = self.client.get(self.all_products,
                                   {"sort": "name"})
        context = response.context
        self.assertTrue(context["current_sorting"])
        self.assertEqual(context["current_sorting"].split("_")[0], "name")

    def test_all_products_view_with_invalid_sort_param(self):
        """
        Test for all Products view with invalid sort parameter
        """
        response = self.client.get(self.all_products,
                                   {"sort": "size"})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "You sort criteria didn't match our records!")

    def test_all_products_view_with_sort_and_direction(self):
        """
        Test for all Products view with sort
        and direction parameter
        """
        response = self.client.get(self.all_products,
                                   {"sort": "name", "direction": "asc"})
        context = response.context
        self.assertTrue(context["current_sorting"])
        self.assertEqual(context["current_sorting"], "name_asc")

    def test_all_products_view_with_sort_by_category(self):
        """
        Test for all Products view with sort by category
        and direction parameter
        """
        response = self.client.get(self.all_products,
                                   {"sort": "category", "direction": "asc"})
        context = response.context
        self.assertTrue(context["current_sorting"])
        self.assertEqual(context["current_sorting"], "category_asc")

    def test_all_products_view_with_sort_by_brand(self):
        """
        Test for all Products view with sort by brand
        and direction parameter
        """
        response = self.client.get(self.all_products,
                                   {"sort": "brand", "direction": "desc"})
        context = response.context
        self.assertTrue(context["current_sorting"])
        self.assertEqual(context["current_sorting"], "brand_desc")

    def test_category_with_sort_by_brand(self):
        """
        Test for all Products from category with no parent - child relation
        with sort by brand and direction parameter
        """
        response = self.client.get(self.products_from_category,
                                   {"sort": "brand", "direction": "desc"})
        context = response.context
        self.assertTrue(context["current_sorting"])
        self.assertEqual(context["current_sorting"], "brand_desc")

    def test_category_parent_with_sort_by_name(self):
        """
        Test for all Products view from parent category with sort by brand
        and direction parameter
        """
        response = self.client.get(self.products_from_category_parent,
                                   {"sort": "name", "direction": "asc"})
        context = response.context
        self.assertTrue(context["current_sorting"])
        self.assertEqual(context["current_sorting"], "name_asc")

    def test_category_child_with_sort_by_price(self):
        """
        Test for all Products view from child category with sort by brand
        and direction parameter
        """
        response = self.client.get(self.products_from_category_child,
                                   {"sort": "price", "direction": "asc"})
        context = response.context
        self.assertTrue(context["current_sorting"])
        self.assertEqual(context["current_sorting"], "price_asc")

    def test_all_products_except_page_not_integer(self):
        """
        Test for all Products view
        """
        response = self.client.get(self.all_products,
                                   {"page": "name"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertTemplateUsed(response, "base.html")

    def test_all_products_except_empty_page(self):
        """
        Test for all Products view for except empty page
        """
        response = self.client.get(self.all_products,
                                   {"page": -1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertTemplateUsed(response, "base.html")

    def test_all_products_valid_page(self):
        """
        Test for all Products view with page parameter
        """
        response = self.client.get(self.all_products,
                                   {"page": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products'].number, 1)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertTemplateUsed(response, "base.html")


class TestProductDetail(TestCase):
    """
    Test for product detail view.
    """

    def setUp(self):
        self.client = Client()
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
        self.product_for_category_child = Product.objects.create(
            sku="2",
            brand="Test",
            name="Test Product Child",
            slug="test-product-child",
            description="Test description child",
            price=4.99,
            category=self.category_child,
            image_url="",
            image="",
            has_sizes=False,
            fields_size=0
        )
        self.product_detail = reverse(
            "product_detail",
            kwargs={"category_slug": self.category.slug,
                    "product_slug": self.product.slug}
        )

    def test_product_detail_view_complete_the_look_none(self):
        """
        Test for Product Detail view
        """
        response = self.client.get(self.product_detail)
        context = response.context
        self.assertFalse(context["complete_the_look"])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")
        self.assertTemplateUsed(response, "base.html")

    def test_product_detail_view_complete_the_look(self):
        """
        Test for Product Detail view
        """
        category = Category.objects.get(name=self.category.name)
        category.name = "2_piece_suits"
        category.save(update_fields=['name'])

        category_child = Category.objects.get(name=self.category_child)
        category_child.name = "shirts"
        category_child.save(update_fields=['name'])

        response = self.client.get(self.product_detail)
        context = response.context
        self.assertTrue(context["complete_the_look"])
        self.assertTemplateUsed(response, "products/product_detail.html")
        self.assertTemplateUsed(response, "base.html")


class TestProductManagementViews(TestCase):
    """
    Test for add, edit and delete product with
    user and super user
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            email='test.user@email.com',
            password='testuserpassword'
        )
        self.super_user = User.objects.create_superuser(
            username='test_admin',
            email='test.admin@email.com',
            password='testadminpassword'
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
        self.all_products = reverse(
            "products"
        )
        self.product_detail = reverse(
            "product_detail",
            kwargs={"category_slug": self.category.slug,
                    "product_slug": self.product.slug}
        )
        self.products_from_category = reverse(
            "products_from_category",
            kwargs={"category_slug": self.category.slug}
        )
        self.add_product = reverse("add_product")
        self.edit_product = reverse(
            "edit_product",
            kwargs={"product_id": self.product.id}
        )
        self.delete_product = reverse(
            "delete_product",
            kwargs={"product_id": self.product.id}
        )
        self.home = reverse("home")

    def test_add_product_user(self):
        """
        Test for Add Product view when user
        is not a superuser
        """
        self.assertTrue(self.client.login(
            username="test_user", password="testuserpassword")
        )
        response = self.client.get(self.add_product)
        self.assertRedirects(response, self.home)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "You don't have permission to access this page.")

    def test_edit_product_user(self):
        """
        Test for Edit Product view when user
        is not a superuser
        """
        self.assertTrue(self.client.login(
            username="test_user", password="testuserpassword")
        )
        response = self.client.get(self.edit_product)
        self.assertRedirects(response, self.home)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "You don't have permission to access this page.")

    def test_delete_product_user(self):
        """
        Test for Delete Product view when user
        is not a superuser
        """
        self.assertTrue(self.client.login(
            username="test_user", password="testuserpassword")
        )
        response = self.client.get(self.delete_product)
        self.assertRedirects(response, self.home)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Sorry, only store owners can do that.")

    def test_add_product_superuser_get_method(self):
        """
        Test for Add Product view with superuser
        for get method
        """
        self.assertTrue(self.client.login(
            username='test_admin', password='testadminpassword')
        )
        response = self.client.get(self.add_product)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/add_product.html")
        self.assertTemplateUsed(response, "base.html")

    def test_add_product_superuser_post_invalid_data(self):
        """
        Test for Add Product view with superuser
        for post method with invalid data
        """
        self.assertTrue(
            self.client.login(
                username='test_admin', password='testadminpassword')
        )
        response = self.client.post(
            self.add_product,
            data={
                'sku': '',
                'brand': '',
                'name': '',
                'slug': '',
                'description': '',
                'price': 7.99,
                'category': self.category.pk,
                'has_sizes': False,
                'fields_size': 0
            })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Failed to add product. "
                         "Please ensure the form is valid.")

    def test_add_product_superuser_post_valid_data(self):
        """
        Test for Add Product view with superuser
        for post method with valid data
        """
        self.assertTrue(
            self.client.login(
                username='test_admin', password='testadminpassword')
        )
        response = self.client.post(
            self.add_product,
            data={
                'sku': 'test01',
                'brand': 'Test post',
                'name': 'Test product post method',
                'slug': 'test-product-post-method',
                'description': 'Test description',
                'price': 5.99,
                'category': self.category.pk,
                'has_sizes': False,
                'fields_size': 0
            })
        product = Product.objects.get(name="Test product post method")
        self.assertTrue(product)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f'/products/{self.category.slug}/{product.slug}/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Successfully added product!")

    def test_edit_product_superuser_get(self):
        """
        Test for Edit Product view with superuser
        for get method
        """
        self.assertTrue(self.client.login(
            username='test_admin', password='testadminpassword')
        )
        response = self.client.get(self.edit_product)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         f'You are editing {self.product.name}')

    def test_edit_product_superuser_post_invalid_data(self):
        """
        Test for Edit Product view with superuser
        for post method with invalid data
        """
        self.assertTrue(
            self.client.login(
                username='test_admin', password='testadminpassword')
            )
        response = self.client.post(
            self.edit_product,
            data={
                'sku': '',
                'brand': '',
                'name': '',
                'slug': '',
                'description': '',
                'price': 5.99,
                'category': self.category.pk,
                'has_sizes': False,
                'fields_size': 0
            })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Failed to update product. '
                         'Please ensure the form is valid.')

    def test_edit_product_superuser_post_valid_data(self):
        """
        Test for Edit Product view with superuser
        for post method with valid data
        """
        self.assertTrue(self.client.login(
            username='test_admin', password='testadminpassword')
        )
        response = self.client.post(
            self.edit_product,
            data={
                'sku': 'test01',
                'brand': 'Test edit product',
                'name': 'Test edit product post method',
                'slug': 'test-product-post-method',
                'description': 'Test description',
                'price': 5.99,
                'category': self.category.pk,
                'has_sizes': False,
                'fields_size': 0
            })
        product = Product.objects.get(name="Test edit product post method")
        self.assertTrue(product)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f'/products/{self.category.slug}/{product.slug}/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Successfully updated product!')

    def test_delete_product_superuser(self):
        """
        Test for Delete Product view with superuser
        for get method
        """
        self.assertTrue(self.client.login(
            username='test_admin', password='testadminpassword')
        )
        response = self.client.get(self.delete_product)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.all_products)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Product deleted!')
