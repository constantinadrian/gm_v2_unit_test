from django.test import TestCase
from django.contrib.auth.models import User

from profiles.models import UserProfile


class TestProfilesModels(TestCase):
    """
    Test for Profiles models
    """

    def setUp(self):
        self.user = User.objects.create(
            username='test_user',
            email='test.user@email.com',
            password='testuserpassword'
        )

    def test_review_model(self):
        """
        Test for profile model
        """
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(str(profile), f"{self.user.username}")
