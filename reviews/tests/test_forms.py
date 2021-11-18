from django.test import TestCase

from reviews.forms import ReviewForm


class TestReviewForms(TestCase):
    """
    Test Reviews forms
    """

    def test_review_form_invalid_data(self):
        """
        Test Review form with invalid data
        """
        form = ReviewForm({
            'title': '',
            'description': '',
            'rating': ''
        })

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors.keys())
        self.assertEqual(form.errors["title"][0], "This field is required.")
        self.assertIn("description", form.errors.keys())
        self.assertEqual(
            form.errors["description"][0], "This field is required."
            )
        self.assertIn("rating", form.errors.keys())
        self.assertEqual(form.errors["rating"][0], "This field is required.")

        self.assertNotIn("user", form.errors.keys())
        self.assertNotIn("product", form.errors.keys())
        self.assertNotIn("date_posted", form.errors.keys())

    def test_review_form_valid_data(self):
        """
        Test Review form with data
        """
        form = ReviewForm({
            'title': 'Review test',
            'description': 'Review description',
            'rating': 5
        })

        self.assertTrue(form.is_valid())
