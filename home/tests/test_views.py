from django.test import TestCase, Client
from django.urls import reverse


class TestHomeViews(TestCase):
    """
    Test for home views
    """
    def setUp(self):
        self.client = Client()
        self.home = reverse('home')

    def test_home_view(self):
        """
        Test for home view
        """
        response = self.client.get(self.home)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
        self.assertTemplateUsed(response, "base.html")
