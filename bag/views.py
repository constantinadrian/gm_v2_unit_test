from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    reverse,
    HttpResponse
)
from products.models import Product
from django.contrib import messages


def view_bag(request):
    """"
    A view to return the shopping bag page.
    Args:
        request : django request object
    Returns:
        rendered bag html
    """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """"
    A view that add a quantity of the specified product to the shopping bag.
    Args:
        request : django request object
        item_id : slug is the part of the URL that is unique
                  for each and every page of a website which
                  identifies a particular product id
    Returns:
        redirect to redirect_url
    """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None

    if product.has_sizes is True and product.fields_size == 1:
        size = request.POST['product_size']

    elif product.has_sizes is True and product.fields_size == 2:
        jacket_size = request.POST['jacket_size']
        trouser_size = request.POST['trouser_size']
        size = "-".join([jacket_size, trouser_size])

    elif product.has_sizes is True and product.fields_size == 3:
        jacket_size = request.POST['jacket_size']
        waistcoat_size = request.POST['waistcoat_size']
        trouser_size = request.POST['trouser_size']
        size = "-".join([jacket_size, waistcoat_size, trouser_size])

    # get that bag from the session if exist
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request,
                                 (f'Updated size {size.upper()} '
                                  f'{product.name} quantity to '
                                  f'{bag[item_id]["items_by_size"][size]}'))
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request,
                                 (f'Added size {size.upper()} '
                                  f'{product.name} to your bag'))
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request,
                             (f'Added size {size.upper()} '
                              f'{product.name} to your bag'))
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request,
                             (f'Updated {product.name} '
                              f'quantity to {bag[item_id]}'))
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """"
    A view that adjust the quantity of the
    specified product to the shopping bag.
    Args:
        request : django request object
        item_id : slug is the part of the URL that is unique
                  for each and every page of a website which
                  identifies a particular product id
    Returns:
        redirect reverse view_bag
    """

    product = get_object_or_404(Product, pk=item_id)

    try:
        quantity = int(request.POST.get('quantity'))
    except ValueError:
        quantity = 1

    size = None

    if 'product_size' in request.POST:
        size = request.POST['product_size']

    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request,
                             (f'Updated size {size.upper()} '
                              f'{product.name} quantity to '
                              f'{bag[item_id]["items_by_size"][size]}'))
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request,
                             (f'Removed size {size.upper()} '
                              f'{product.name} from your bag'))
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request,
                             (f'Updated {product.name} '
                              f'quantity to {bag[item_id]}'))
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """"
    A view that remove the specified product to the shopping bag.
    Args:
        request : django request object
        item_id : slug is the part of the URL that is unique
                  for each and every page of a website which
                  identifies a particular product id
    Returns:
        HttpResponse status=200
    Except:
        HttpResponse status=500
    """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request,
                             (f'Removed size {size.upper()} '
                              f'{product.name} from your bag'))
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
