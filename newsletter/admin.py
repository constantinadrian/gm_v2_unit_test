from django.contrib import admin
from .models import Newsletter


class NewsletterAdmin(admin.ModelAdmin):
    readonly_fields = ('email',
                       'subscription_date',)

    list_display = ('email',
                    'subscription_date',)

    ordering = ('-subscription_date',)


admin.site.register(Newsletter, NewsletterAdmin)
