from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse

from products.models import Category, Product


class TestBagViews(TestCase):
    """
    Test for bag views
    """
    def setUp(self):
        self.client = Client()
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
        self.product1 = Product.objects.create(
            sku="2",
            brand="Test",
            name="Test Product One",
            slug="test-product-one",
            description="Test description one",
            price=4.99,
            category=self.category,
            image_url="",
            image="",
            has_sizes=True,
            fields_size=1
        )
        self.product2 = Product.objects.create(
            sku="3",
            brand="Test",
            name="Test Product Two",
            slug="test-product-two",
            description="Test description two",
            price=7.99,
            category=self.category,
            image_url="",
            image="",
            has_sizes=False,
            fields_size=0
        )
        self.bag = reverse('view_bag')
        self.add_to_bag = reverse(
            'add_to_bag',
            kwargs={'item_id': self.product.pk}
        )
        self.add_to_bag1 = reverse(
            'add_to_bag',
            kwargs={'item_id': self.product1.pk}
        )
        self.add_to_bag2 = reverse(
            'add_to_bag',
            kwargs={'item_id': self.product2.pk}
        )
        self.adjust_bag = reverse(
            'adjust_bag',
            kwargs={'item_id': self.product.pk}
        )
        self.adjust_bag2 = reverse(
            'adjust_bag',
            kwargs={'item_id': self.product2.pk}
        )
        self.remove_from_bag = reverse(
            'remove_from_bag',
            kwargs={'item_id': self.product.pk}
        )
        self.remove_from_bag2 = reverse(
            'remove_from_bag',
            kwargs={'item_id': self.product2.pk}
        )

    def test_view_bag_view(self):
        """
        Test view bag view
        """
        response = self.client.get(self.bag)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('bag/bag.html')
        self.assertTemplateUsed('base.html')

    def test_add_to_bag_post(self):
        """
        Test add to bag view post method for product with size
        """
        size = '32'
        response = self.client.post(
            self.add_to_bag,
            data={
                'quantity': '1',
                'product_size': size,
                'redirect_url': '/',
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Added size {size.upper()} '
            f'{self.product.name} to your bag'
            )

    def test_add_to_bag_post_value_error(self):
        """
        Test add to bag view, post method, with quantity
        value error
        """
        response = self.client.post(
            self.add_to_bag,
            data={
                'quantity': 'a',
                'product_size': '32',
                'redirect_url': '/',
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_add_to_bag_post_update_product_no_size_session_bag(self):
        """
        Test add to bag view, post method, update quantity
        to product with no size in session bag
        """
        bag = {'3': 1}
        session = self.client.session
        session['bag'] = bag
        session.save()
        response = self.client.post(
            self.add_to_bag2,
            data={
                'quantity': '5',
                'redirect_url': '/',
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        r_session = self.client.session
        r_bag = r_session['bag']
        r_quantity = r_bag['3']
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Updated {self.product2.name} '
            f'quantity to {r_quantity}'
            )

    def test_add_to_bag_post_update_quantity_session_bag(self):
        """
        Test add to bag view, post method, update quantity
        to product with size in session bag
        """
        size = '32'
        bag = {'1': {'items_by_size': {size: 1}}}
        session = self.client.session
        session['bag'] = bag
        session.save()
        response = self.client.post(
            self.add_to_bag,
            data={
                'quantity': '1',
                'product_size': size,
                'redirect_url': '/',
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        r_session = self.client.session
        r_bag = r_session['bag']
        r_size = r_bag['1']['items_by_size'][size]
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Updated size {size.upper()} '
            f'{self.product.name} quantity to '
            f'{r_size}'
        )

    def test_add_to_bag_post_different_size_session_bag(self):
        """
        Test add to bag view, post method, adding different
        size of product to session bag
        """
        size = '34'
        bag = {'1': {'items_by_size': {'32': 1}}}
        session = self.client.session
        session['bag'] = bag
        session.save()
        response = self.client.post(
            self.add_to_bag,
            data={
                'quantity': '3',
                'product_size': size,
                'redirect_url': '/',
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        r_session = self.client.session
        r_bag = r_session['bag']
        r_size = r_bag['1']['items_by_size'][size]
        self.assertTrue(r_size, '3')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Added size {size.upper()} '
            f'{self.product.name} to your bag'
            )

    def test_add_to_bag_post_new_product_with_session_bag(self):
        """
        Test add to bag view, post method, adding new
        product to bag session
        """
        size = '34'
        bag = {'1': {'items_by_size': {size: 1}}}
        session = self.client.session
        session['bag'] = bag
        session.save()
        response = self.client.post(
            self.add_to_bag1,
            data={
                'quantity': '2',
                'product_size': size,
                'redirect_url': '/',
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        r_session = self.client.session
        r_bag = r_session['bag']
        r_size = r_bag['2']['items_by_size'][size]
        self.assertTrue(r_size, '2')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Added size {size.upper()} '
            f'{self.product1.name} to your bag'
            )

    def test_adjust_bag_update_size_product_from_session_bag(self):
        """
        Test adjust_bag view, post method, adding more
        quantity to product with size from bag session
        """
        size = '34'
        bag = {'1': {'items_by_size': {size: 1}}}
        session = self.client.session
        session['bag'] = bag
        session.save()
        response = self.client.post(
            self.adjust_bag,
            data={
                'quantity': '2',
                'product_size': size
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.bag)
        r_session = self.client.session
        r_bag = r_session['bag']
        r_size = r_bag['1']['items_by_size'][size]
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Updated size {size.upper()} '
            f'{self.product.name} quantity to '
            f'{r_size}'
            )

    def test_adjust_bag_remove_size_product_from_session_bag(self):
        """
        Test adjust_bag view, post method, remove product with size
        when quantity is zero, from bag session
        """
        size = '34'
        bag = {'1': {'items_by_size': {size: 1}}}
        session = self.client.session
        session['bag'] = bag
        session.save()
        response = self.client.post(
            self.adjust_bag,
            data={
                'quantity': '0',
                'product_size': size
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.bag)
        r_session = self.client.session
        r_bag = r_session['bag']
        self.assertEqual(r_bag, {})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Removed size {size.upper()} '
            f'{self.product.name} from your bag'
            )

    def test_adjust_bag_update_nosize_product_from_session_bag(self):
        """
        Test adjust_bag view, post method, adding more
        quantity to product with no size from bag session
        """
        bag = {'3': 1}
        session = self.client.session
        session['bag'] = bag
        session.save()
        response = self.client.post(
            self.adjust_bag2,
            data={
                'quantity': '2',
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.bag)
        r_session = self.client.session
        r_bag = r_session['bag']
        r_quantity = r_bag['3']
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Updated {self.product2.name} '
            f'quantity to {r_quantity}'
            )

    def test_adjust_bag_remove_nosize_product_from_session_bag(self):
        """
        Test adjust_bag view, post method, remove product with size
        when quantity is zero, from bag session
        """
        bag = {'3': 1}
        session = self.client.session
        session['bag'] = bag
        session.save()
        response = self.client.post(
            self.adjust_bag2,
            data={
                'quantity': '0',
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.bag)
        r_session = self.client.session
        r_bag = r_session['bag']
        self.assertEqual(r_bag, {})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Removed {self.product2.name} from your bag'
            )

    def test_adjust_bag_quantity_value_error(self):
        """
        Test adjust_bag view, post method, quantity value error
        """
        bag = {'3': 1}
        session = self.client.session
        session['bag'] = bag
        session.save()
        response = self.client.post(
            self.adjust_bag2,
            data={
                'quantity': 'v',
            })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.bag)
        r_session = self.client.session
        r_bag = r_session['bag']
        r_quantity = r_bag['3']
        self.assertEqual(r_quantity, 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Updated {self.product2.name} '
            f'quantity to {r_quantity}'
            )

    def test_remove_from_bag_size_product_from_session_bag(self):
        """
        Test remove_from_bag view, post method, remove
        product with size from bag session
        """
        size = '34'
        bag = {'1': {'items_by_size': {size: 1}}}
        session = self.client.session
        session['bag'] = bag
        session.save()
        response = self.client.post(
            self.remove_from_bag,
            data={
                'product_size': size
            })
        self.assertEqual(response.status_code, 200)
        r_session = self.client.session
        r_bag = r_session['bag']
        self.assertEqual(r_bag, {})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Removed size {size.upper()} '
            f'{self.product.name} from your bag'
            )

    def test_remove_from_bag_nosize_product_from_session_bag(self):
        """
        Test remove_from_bag view, post method, remove
        product with no size from bag session
        """
        bag = {'3': 1}
        session = self.client.session
        session['bag'] = bag
        session.save()
        response = self.client.post(self.remove_from_bag2)
        self.assertEqual(response.status_code, 200)
        r_session = self.client.session
        r_bag = r_session['bag']
        self.assertEqual(r_bag, {})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Removed {self.product2.name} from your bag'
            )

    def test_remove_from_bag_exception_500(self):
        """
        Test remove_from_bag view exception 500, remove an item that does exist
        in the session bag
        """
        bag = {'3': 1}
        session = self.client.session
        session['bag'] = bag
        session.save()
        response = self.client.post(
            self.remove_from_bag,
            data={
                'product_size': '32'
            })
        self.assertEqual(response.status_code, 500)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f"Error removing item: '{self.product.pk}'"
            )
