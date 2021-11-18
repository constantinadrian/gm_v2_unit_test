from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

from profiles.models import UserProfile
from reviews.models import Review
from products.models import Category, Product


class TestReviewsViews(TestCase):
    """
    Test for all review view, add,
    remove and delete review
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            email='test.user@email.com',
            password='testuserpassword'
        )
        self.user_two = User.objects.create_user(
            username='test_user_two',
            email='test.user.two@email.com',
            password='testusertwopassword'
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
        self.user_two_review = Review.objects.create(
            user=UserProfile(self.user_two.pk),
            product=self.product,
            title='Test Product Review',
            description='Test Description Review',
            rating=5
        )
        self.review = reverse('reviews')
        self.add_review = reverse(
            'add_review',
            kwargs={'product_slug': self.product.slug}
        )
        self.edit_review = reverse(
            'edit_review',
            kwargs={'review_id': self.user_two_review.pk}
        )
        self.delete_review = reverse(
            'delete_review',
            kwargs={'review_id': self.user_two_review.pk}
        )
        self.account_login = reverse('account_login')
        self.home = reverse('home')

    def test_reviews_view_(self):
        """
        Test for review view
        """
        response = self.client.get(self.review)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/reviews.html")
        self.assertTemplateUsed(response, "base.html")

    def test_reviews_view_with_sort_by_name(self):
        """
        Test for reviews view with sort by name parameter
        """
        response = self.client.get(self.review,
                                   {"sort": "name"})
        context = response.context
        self.assertTrue(context["current_sorting"])
        self.assertEqual(context["current_sorting"].split("_")[0], "name")

    def test_review_view_with_sort_and_direction(self):
        """
        Test for review view with sort
        and direction parameter
        """
        response = self.client.get(self.review,
                                   {"sort": "name", "direction": "desc"})
        context = response.context
        self.assertTrue(context["current_sorting"])
        self.assertEqual(context["current_sorting"], "name_desc")

    def test_reviews_except_empty_page(self):
        """
        Test for review view for except empty page
        """
        response = self.client.get(self.review,
                                   {"page": -1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/reviews.html")
        self.assertTemplateUsed(response, "base.html")

    def test_add_review_anonymous_user(self):
        """
        Test for Add Review view with anonymous user
        """
        response = self.client.get(self.add_review)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'{self.account_login}?next=/reviews/add_review/test-product/'
        )

    def test_add_review_auth_user_get(self):
        """
        Test for Add Review view with auth user for GET method
        """
        self.assertTrue(self.client.login(
            username="test_user", password="testuserpassword")
        )
        response = self.client.get(self.add_review)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/add_review.html")
        self.assertTemplateUsed(response, "base.html")

    def test_add_review_auth_user_invalid_data(self):
        """
        Test for add Review view with auth user with invalid data
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        response = self.client.post(
            self.add_review,
            data={
                'user': self.user,
                'product': self.product,
                'title': '',
                'description': '',
                'rating': 5
            })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Failed to add review to product. '
            'Please ensure the form is valid.'
            )

    def test_add_review_auth_user_post_valid_data(self):
        """
        Test for Add Review view with auth user for POST method
        with valid data
        """
        self.assertTrue(
            self.client.login(
                username="test_user", password="testuserpassword")
            )
        response = self.client.post(
            self.add_review,
            data={
                'user': self.user,
                'product': self.product,
                'title': 'Test review post method',
                'description': 'Test description',
                'rating': 5
            })
        review = Review.objects.get(title="Test review post method")
        self.assertTrue(review)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f'/reviews/add_review/{self.product.slug}/'
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Successfully added review '
            f'to {self.product.name}'
            )

    def test_edit_review_auth_different_user_get(self):
        """
        Test for Edit review for get method with
        different user
        """
        self.assertTrue(
            self.client.login(
                username='test_user',
                password='testuserpassword')
            )
        response = self.client.get(self.edit_review)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Sorry, this review does not belong to you.'
            )

    def test_edit_review_auth_user_get(self):
        """
        Test for Edit review for get method
        """
        self.assertTrue(
            self.client.login(
                username='test_user_two',
                password='testusertwopassword')
            )
        response = self.client.get(self.edit_review)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'You are editing {self.product.name} review.'
            )

    def test_edit_review_auth_user_post_invalid_data(self):
        """
        Test for Edit review for post method with invalid data
        """
        self.assertTrue(
            self.client.login(
                username='test_user_two',
                password='testusertwopassword')
            )
        response = self.client.post(
            self.edit_review,
            data={
                'user': self.user,
                'product': self.product,
                'title': '',
                'description': '',
                'rating': 5
            })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Failed to update review to product. '
            'Please ensure the form is valid.'
            )

    def test_edit_review_auth_user_post_valid_data(self):
        """
        Test for Edit review for post method with valid data
        """
        self.assertTrue(
            self.client.login(
                username='test_user_two',
                password='testusertwopassword')
            )
        response = self.client.post(
            self.edit_review,
            data={
                'user': self.user,
                'product': self.product,
                'title': 'Test edit review',
                'description': 'Test edit description',
                'rating': 5
            })
        review = Review.objects.get(title="Test edit review")
        self.assertTrue(review)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'/products/{self.category.slug}/{self.product.slug}/'
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            f'Successfully updated review '
            f'to {self.product.name}'
            )

    def test_delete_review_auth_different_user_get(self):
        """
        Test for Delete review for get method with
        different user
        """
        self.assertTrue(
            self.client.login(
                username='test_user',
                password='testuserpassword')
            )
        response = self.client.get(self.delete_review)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Sorry, only the owner can delete his review.'
            )

    def test_delete_review_auth_user_get(self):
        """
        Test for Delete review for get method with
        different user
        """
        self.assertTrue(
            self.client.login(
                username='test_user_two',
                password='testusertwopassword')
            )
        response = self.client.get(self.delete_review)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.review)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Review deleted!')
