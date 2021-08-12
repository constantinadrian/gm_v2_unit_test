from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):

    list_display = ('user', 'product', 'title',
                    'description', 'rating',
                    'date_posted',)

    ordering = ('-date_posted',)


admin.site.register(Review, ReviewAdmin)
