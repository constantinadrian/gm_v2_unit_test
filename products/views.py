from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Q
from random import shuffle
from django.contrib import messages
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, Category
from .forms import ProductForm


def all_products(request, category_slug=None):
    """"
    A view to show all products, including sorting and search queries.
    Args:
        request : django request object
        category_slug : part of a URL that is unique which
                        identifies a particular group of related products
    Returns:
        rendered products html
    """

    products = Product.objects.all().order_by('id')
    query = None
    category = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey

            # check if sort in one of the db fields
            sortkey_check = getattr(Product, sortkey, False)

            # if sortkey does not exist, redirect to the
            # product page to avoid a 500 server error
            if sortkey_check is False:
                messages.error(request,
                               "You sort criteria didn't match our records!")
                return redirect(reverse('products'))

            # to allow case insensitive on name field
            # annotate all products with a new field
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if sortkey == 'category':
                sortkey = 'category__name'

            if sortkey == 'brand':
                sortkey = 'brand'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                # if direction is desc reverse the order
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)

        # check if user was on a specific category/subcategory
        # then filter the all sorts products
        # to show the products from that specific category/subcategory
        if category_slug is not None:
            # check if category slug from url exist in category db
            category = get_object_or_404(Category, slug=category_slug)

            # check if category is a child of other category
            if category.parent is not None:
                # if child show producs from this category
                products = products.filter(category__name=category.name)
            else:
                # check if category is a parrent or
                # just a normal category (no parent and no child category)
                parent_category = Category.objects.filter(
                        parent=category.id).count()

                # if parent, show all products from his children
                if parent_category:
                    products = products.filter(category__parent=category.id)

                # show products from requested normal category
                else:
                    products = products.filter(category__name=category.name)

            # query again the category for
            # badge button filter on product page
            category = category = Category.objects.filter(name=category.name)

        # if there is a search query attach to get method filter
        # the products base on the search query
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = (Q(name__icontains=query) |
                       Q(brand__icontains=query) |
                       Q(description__icontains=query))
            products = products.filter(queries)

    else:
        # check if user navigate on a specific category/subcategory
        # to show the products from that specific category/subcategory
        if category_slug is not None:
            # check if category slug from url exist in category db
            category = get_object_or_404(Category, slug=category_slug)

            # check if category is a child of other category
            if category.parent is not None:
                # if child show producs from this category
                products = products.filter(category__name=category.name)
            else:
                # check if category is a parrent or
                # just a normal category (no parent and no child category)
                parent_category = Category.objects.filter(
                        parent=category.id).count()

                # if parent, show all products from his children
                if parent_category:
                    products = products.filter(category__parent=category.id)

                # show products from requested normal category
                else:
                    products = products.filter(category__name=category.name)

            # query again the category for
            # badge button filter on product page
            category = Category.objects.filter(name=category.name)

    current_sorting = f'{sort}_{direction}'

    # Pagination show 12 products per page
    paginator = Paginator(products, 12)

    page = request.GET.get('page')
    try:
        all_products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        all_products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_products = paginator.page(paginator.num_pages)

    # Pagination was inspired, modified and
    # adapted to this project from from this
    # # Credit code
    # https://www.youtube.com/watch?v=MAIFJ3_bcCY
    index = all_products.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'products': all_products,
        'page_range': page_range,
        'search_term': query,
        'current_categories': category,
        'current_sorting': current_sorting,
    }

    return render(request, "products/products.html", context)


def product_detail(request, category_slug, product_slug):
    """"
    A view to show individual product details.
    Args:
        request : django request object
        category_slug : part of a URL that is unique which
                        identifies a particular group of related products
        product_slug : slug is the part of the URL that is unique
                       for each and every page of a website which
                       identifies a particular product
    Returns:
        rendered product_detail html
    """

    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category__slug=category_slug,
                                slug=product_slug)

    complete_the_look = None
    you_might_also_like = None

    if ((category.name == "2_piece_suits") or
            (category.name == "3_piece_suits") or
            (category.name == "tuxedos")):
        queries = Q(category__name__icontains="shirts") | Q(
                  category__name__icontains="shoes")

        complete_the_look = list(Product.objects.all().filter(queries))
        shuffle(complete_the_look)

        you_might_also_like = list(Product.objects.all().filter(
                                   category__slug=category_slug))

        shuffle(you_might_also_like)
    else:
        you_might_also_like = list(Product.objects.all().filter(
                                   category__slug=category_slug))
        shuffle(you_might_also_like)

    context = {
        'product': product,
        'complete_the_look': complete_the_look,
        'you_might_also_like': you_might_also_like,
    }

    return render(request, "products/product_detail.html", context)


@login_required
def add_product(request):
    """
    A view to show the added product to the store
    Args:
        request : django request object
    Returns:
        rendered add_product html
    """

    if not request.user.is_superuser:
        messages.error(
            request, 'You don\'t have permission to access this page.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        # Check if the form is valid with helper function
        response = check_form(request)
        if response['valid']:
            messages.success(request, 'Successfully added product!')
            return redirect(
                reverse('product_detail',
                        kwargs={
                            'category_slug': response['product'].category.slug,
                            'product_slug': response['product'].slug}))
        else:
            form = response['form']
            messages.error(request,
                           ('Failed to add product. '
                            'Please ensure the form is valid.'))
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
        'product_management': True,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    A view to show the updated product to the store
    Args:
        request : django request object
        product_id : slug is the part of the URL that is unique
                     for each and every page of a website which
                     identifies a particular product id
    Returns:
        rendered edit_product html
    """

    product = get_object_or_404(Product, pk=product_id)

    if not request.user.is_superuser:
        messages.error(request, ('You don\'t have permission '
                                 'to access this page.'))
        return redirect(reverse('home'))

    if request.method == 'POST':
        # Check if the form is valid with helper function
        response = check_form(request, product)
        if response['valid']:
            messages.success(request, 'Successfully updated product!')
            return redirect(
                reverse('product_detail',
                        kwargs={'category_slug': product.category.slug,
                                'product_slug': product.slug}))
        else:
            form = response['form']
            messages.error(request,
                           ('Failed to update product. '
                            'Please ensure the form is valid.'))
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
        'product_management': True,
    }

    return render(request, template, context)


def check_form(request, product=None):
    """
    A helper function that checks if the
    form is valid on POST request for add product
    and edit product views
    Args:
        request : django request object
        product : product instance that needs to be
        validated with the form
    Returns:
        True: For edit product view: return a dict with valid response
              For add product view: return a dict with valid response
                                    and instance of product
        False: Return a dict with invalid response and the form instance
               for both of the add and edit views
    """
    if product:
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return {'valid': True}

    else:
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return {'valid': True, 'product': product}

    return {'valid': False, 'form': form}


@login_required
def delete_product(request, product_id):
    """
    A view to delete a product from the store
    Args:
        request : django request object
        product_id : slug is the part of the URL that is unique
                     for each and every page of a website which
                     identifies a particular product id
    Returns:
        redirect reverse products
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')

    return redirect(reverse('products'))
