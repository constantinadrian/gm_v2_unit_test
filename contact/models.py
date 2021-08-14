from django.db import models


class Contact(models.Model):
    """
    Contact model so users can contact the store owner
    """

    class Meta:
        ordering = ("-sent_date",)

    name = models.CharField(max_length=254)
    email = models.EmailField()
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
