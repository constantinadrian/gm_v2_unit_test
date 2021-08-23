from django.db import models


class Newsletter(models.Model):
    """
    Newsletter model that stores users email
    """
    class Meta:
        verbose_name_plural = "Newsletters"

        ordering = ("-subscription_date",)

    email = models.EmailField()
    subscription_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
