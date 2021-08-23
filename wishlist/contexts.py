from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from .models import Wishlist


def user_wishlist(request):
    """
    Context processor to access all products from user wishlist
    Args:
        request : django request object
    Returns:
        context
    """
    if request.user.is_authenticated:
        wishlist = get_object_or_404(Wishlist, user=request.user)

        # Pagination show 12 products per page
        paginator = Paginator(wishlist.products.all().order_by('id'), 12)

        page = request.GET.get('page')
        try:
            all_wishlist = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            all_wishlist = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
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

        context = {'wishlist': all_wishlist,
                   'page_range': page_range, }

    else:
        context = {
            'wishlist': [],
        }

    return context
