from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Product, Category
from django.db.models import Q
from random import shuffle
from django.contrib import messages


def all_products(request, category_slug=None):
    """" A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    category = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            # to allow case insensitive on name field
            # annotate all products with a new field
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                # if direction is desc reverse the order
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            products = products.order_by(sortkey)

            category = Category.objects.filter(parent=None)

        if category_slug is not None:
            category = get_object_or_404(Category, slug=category_slug)
            if category.parrent is not None:
                products = products.filter(category__parrent__in=category.id)
            else:
                products = products.filter(category__name__in=category.name)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = (Q(name__icontains=query) |
                       Q(description__icontains=query))
            products = products.filter(queries)

    else:
        if category_slug is not None:
            category = get_object_or_404(Category, slug=category_slug)
            # check if category is a child of other category
            if category.parent is not None:
                products = products.filter(category__name=category.name)
            else:
                # products = products.filter(category__parent=category.id)
                # check if category is a parrent or just a normal category
                # if products.count() == 0:
                #     products = Product.objects.all().filter(category__name=category.name)
                parent_category = Category.objects.filter(
                        parent=category.id).count()

                if parent_category:
                    products = products.filter(category__parent=category.id)
                else:
                    products = products.filter(category__name=category.name)

            category = Category.objects.filter(name=category.name)
        else:
            category = Category.objects.filter(parent=None)

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
    """" A view to show individual product details """

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
