from django.test import TestCase
from django.urls import reverse, resolve

from reviews.views import (
    reviews, add_review,
    edit_review, delete_review
)


class TestReviewUrls(TestCase):
    """
    Test for Urls for reviews app
    """

    def test_all_reviews_urls(self):
        """
        Test for Url for all reviews
        """
        url = reverse('reviews')
        self.assertEqual(resolve(url).func, reviews)

    def test_add_review_urls(self):
        """
        Test for add review Url
        """
        url = reverse(
            'add_review',
            kwargs={'product_slug': 'product'}
        )
        self.assertEqual(resolve(url).func, add_review)

    def test_edit_review_urls(self):
        """
        Test for edit review Url
        """
        url = reverse(
            'edit_review',
            kwargs={'review_id': '1'}
        )
        self.assertEqual(resolve(url).func, edit_review)

    def test_delete_reviews_urls(self):
        """
        Test for delete review Url
        """
        url = reverse(
            'delete_review',
            kwargs={'review_id': '1'}
        )
        self.assertEqual(resolve(url).func, delete_review)
