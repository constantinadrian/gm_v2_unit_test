from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    # Inline item is going to allow us to add and edit line items
    # in the admin right from inside the order model, rather
    # than having to go to the order line item interface
    model = OrderLineItem
    # Readonly fields to not compromise the integrity of an order
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    # Add inline option in the Order class
    inlines = (OrderLineItemAdminInline,)

    # Readonly fields to not compromise the integrity of an order
    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_bag',
                       'stripe_pid',)

    # Fiedls option to specified the order of the fields in admin
    # interface to avoid the fields adjusted by django due to the
    # use of some read-only fields
    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_bag',
              'stripe_pid',)

    # Restrict the columns that show up in the order list
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',)


# Register the Order model and the OrderAdmin only,
# because the OrderLineItem model will be accessible
# via the inline on the order model
admin.site.register(Order, OrderAdmin)
