from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Product


class Wishlist(models.Model):
    """
    Wishlist Class model base on the profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_the_UserWishlist(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        Wishlist.objects.create(user=instance)
    instance.userprofile.save()
