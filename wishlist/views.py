from django.shortcuts import (
    render,
    get_object_or_404,
    HttpResponse
)
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages

from products.models import Product
from .models import Wishlist


def wishlist(request):
    """"
    A view to return the wishlist page
    Args:
        request : django request object
    Returns:
        rendered wishlist html
    """

    return render(request, "wishlist/wishlist.html")


@login_required
def add_to_wishlist(request, product_id):
    """"
    A view that add / remove products from wishlist page
    Args:
        request : django request object
        product_id : slug is the part of the URL that is unique
                     for each and every page of a website which
                     identifies a particular product id
    Returns:
        HttpResponse status=200
    Raises:
        Http404: Page not found.
    """

    if request.method == 'POST':
        # check if product exist in our database
        product = get_object_or_404(Product, pk=product_id)

        # get the wishlist for the login user
        wishlist = get_object_or_404(Wishlist, user=request.user)

        # add product if is not on the list
        if product not in wishlist.products.all():
            wishlist.products.add(product)
            messages.success(request,
                             (f'{product.name} has been '
                              'added to your wishlist.'))
            return HttpResponse(status=200)
        # remove the product if is on the list
        else:
            try:
                wishlist.products.remove(product)
                messages.success(request,
                                 (f'{product.name} has been '
                                  'remove to your wishlist.'))
                return HttpResponse(status=200)
            except Exception as error:
                messages.error(request, f"Error removing product {error}")
                return HttpResponse(status=500)
    # if request is GET show page not found instead
    else:
        raise Http404
