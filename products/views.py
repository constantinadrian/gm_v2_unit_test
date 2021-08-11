from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Product, Category
from django.db.models import Q
from random import shuffle
from django.contrib import messages
from django.db.models.functions import Lower
from .forms import ProductForm


def all_products(request, category_slug=None):
    """"
    A view to show all products, including sorting and search queries.
    This view has been copied, modified and adapted from the Boutique
    Ado project
    """

    products = Product.objects.all()
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
        else:
            # category = Category.objects.filter(parent=None)

            products = list(products)
            shuffle(products)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': category,
        'current_sorting': current_sorting,
    }

    return render(request, "products/products.html", context)


def product_detail(request, category_slug, product_slug):
    """"
    A view to show individual product details.
    This view has been copied, modified and adapted from the Boutique
    Ado project
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


def add_product(request):
    """
    Add a product to the store
    """
    form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
