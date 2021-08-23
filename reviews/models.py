from django.db import models
from profiles.models import UserProfile
from products.models import Product


class Review(models.Model):
    """
    Model that stores a review,
    related to :model:`profiles.userprofile`
    and to :model:`products.product`
    """

    class Meta:
        verbose_name_plural = "Reviews"
        ordering = ("-date_posted",)

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

    def get_each_display_rating(self):
        """
        Get the each rating for
        rendering the 5 star rating
        """
        return self.rating * 100 / 5
