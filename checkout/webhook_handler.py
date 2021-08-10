import json
import time

from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe

        Here we also create an order in case the form isn't
        submitted for some reason
        """
        # get the data from the metadata we store in cache_checkout_data view
        intent = event.data.object

        # payment_intent_id
        pid = intent.id

        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # replace empty strings in the shipping details with none
        # to ensure data is in the same form as database
        for field, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = shipping_details.address.line1
                profile.default_street_address2 = shipping_details.address.line2
                profile.default_county = shipping_details.address.state
                profile.save()

        # check if the order exist
        order_exist = False

        # create a delay for webhook to try to find the order
        # this is in case the webhook handler won't find the order
        # when it first gets the webhook from stripe
        # and to avoid creating two orders in database
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )

                order_exist = True
                break
            except Order.DoesNotExist:
                # this will cause the webhook handler to try to find
                # the order five times over five seconds
                attempt += 1
                time.sleep(1)
        if order_exist:
            return HttpResponse(
                    content=(f'Webhook received: {event["type"]} | SUCCESS: '
                             'Verified order already in database'),
                    status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # iterate through the bag items to create each line item
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        size_items = item_data['items_by_size']
                        for size, quantity in size_items.items():

                            if (product.has_sizes is True and
                                    product.fields_size == 1):
                                order_line_item = OrderLineItem(
                                    order=order,
                                    product=product,
                                    quantity=quantity,
                                    product_size=size,
                                )
                                order_line_item.save()

                            elif (product.has_sizes is True and
                                    product.fields_size == 2):
                                sizes = size.split("-")
                                order_line_item = OrderLineItem(
                                    order=order,
                                    product=product,
                                    quantity=quantity,
                                    jacket_size=sizes[0],
                                    trouser_size=sizes[1],
                                )
                                order_line_item.save()

                            elif (product.has_sizes is True and
                                    product.fields_size == 3):
                                sizes = size.split("-")
                                order_line_item = OrderLineItem(
                                    order=order,
                                    product=product,
                                    quantity=quantity,
                                    jacket_size=sizes[0],
                                    waistcoat_size=sizes[1],
                                    trouser_size=sizes[2],
                                )
                                order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                # return a 500 server error response to stripe
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        return HttpResponse(
                content=(f'Webhook received: {event["type"]} | SUCCESS: '
                         'Created order in webhook'),
                status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
