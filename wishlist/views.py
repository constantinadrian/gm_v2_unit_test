from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from django.http import Http404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from products.models import Product
from .models import Wishlist


def wishlist(request):
    """" A view to return the wishlist page """

    context = {}

    if request.user.is_authenticated:
        wishlist = get_object_or_404(Wishlist, user=request.user)

        # Pagination show 12 products per page
        paginator = Paginator(wishlist.products.all(), 12)

        page = request.GET.get('page')
        try:
            all_wishlist = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            all_wishlist = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            all_wishlist = paginator.page(paginator.num_pages)

        # Pagination was inspired, modified and
        # adapted to this project from from this
        # # Credit code
        # https://www.youtube.com/watch?v=MAIFJ3_bcCY
        index = all_wishlist.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = paginator.page_range[start_index:end_index]

        context = {
            'wishlist': all_wishlist,
            'page_range': page_range,
        }

    template = "wishlist/wishlist.html"

    return render(request, template, context)


def add_to_wishlist(request, product_id):
    print('wishlist view')

    if request.method == 'POST':
        # check if product exist in our database
        product = get_object_or_404(Product, pk=product_id)

        # get the wishlist for the login user
        wishlist = get_object_or_404(Wishlist, user=request.user)

        # add product if is not on the list
        if product not in wishlist.products.all():
            wishlist.products.add(product)
            messages.success(request,
                             f"{product.name} has been added to your wishlist.")
            return HttpResponse(status=200)
        # remove the product if is on the list
        else:
            try:
                wishlist.products.remove(product)
                messages.success(request,
                                 f"{product.name} has been remove to your wishlist.")
                return HttpResponse(status=200)
            except Exception as error:
                messages.error(request, f"Error removing product {error}")
                return HttpResponse(status=500)
    # if request is GET show page not found instead
    else:
        raise Http404
