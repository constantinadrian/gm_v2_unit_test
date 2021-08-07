from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, Category
from django.contrib import messages


def view_bag(request):
    """"
    A view to return the bag contents page.
    This view has been copied from the Boutique
    Ado project
    """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """"
    Add a quantity of the specified product to the shopping bag.
    This view has been copied, modified and adapted from the Boutique
    Ado project
    """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    reddirect_url = request.POST.get('redirect_url')
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

    return redirect(reddirect_url)
