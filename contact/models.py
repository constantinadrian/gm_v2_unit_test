from django.db import models

from profiles.models import UserProfile


class Contact(models.Model):
    """
    Contact model so users can contact the store owner
    """

    class Meta:
        ordering = ("-sent_date",)

    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='userquery')
    name = models.CharField(max_length=254)
    email = models.EmailField()
    subject = models.CharField(max_length=254)
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
