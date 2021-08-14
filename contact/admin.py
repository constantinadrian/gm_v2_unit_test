from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'email', 'message',
                       'sent_date',)

    list_display = ('name', 'email', 'message',
                    'sent_date',)

    ordering = ('-sent_date',)


admin.site.register(Contact, ContactAdmin)
