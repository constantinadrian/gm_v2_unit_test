from django.db import models
from profiles.models import UserProfile
from products.models import Product
from django.db.models import Avg


class Review(models.Model):
    """
    Review model for each user on a specific product
    """

    class Meta:
        verbose_name_plural = "Reviews"
        ordering = ("date_posted",)

    RATE = [
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    ]

    user = models.ForeignKey(UserProfile, related_name="reviews",
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="reviews",
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.IntegerField(choices=RATE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.product}"

    def get_average_rating(self):
        """
        Get the average ratings of each product
        """
        ratings = Review.objects.filter(product=self.product).aggregate(
            avg_rating=Avg("rating")
        )

        return ratings["avg_rating"] or 0

    def get_display_average_rating(self):
        """
        Get the average rating in procentage for
        rendering the 5 star rating
        """
        return self.get_average_rating() * 100 / 5
