from django.test import TestCase
from django.contrib.auth.models import User

from profiles.models import UserProfile
from products.models import Category, Product

from reviews.models import Review


class TestReviewModels(TestCase):
    """
    Test for Reviews models
    """

    def setUp(self):
        self.user = User.objects.create(
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
        self.product=Product.objects.create(
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
        self.user_review = Review.objects.create(
            user=UserProfile(self.user.pk),
            product=self.product,
            title='Test Product Review',
            description='Test Description Review',
            rating=5
        )

    def test_review_model(self):
        """
        Test for review model
        """
        review = Review.objects.get(user=UserProfile(self.user.pk))
        self.assertEqual(str(review), f"{self.user}: {self.product}")
