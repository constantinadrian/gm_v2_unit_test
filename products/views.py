from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def all_products(request):
    """" A view to show all products, including sorting and search queries """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, "products/products.html", context)


def product_detail(request, category_slug, product_slug):
    """" A view to show individual product details """

    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category__slug=category_slug, 
                                slug=product_slug)

    context = {
        'category': category,
        'product': product,
    }

    return render(request, "products/product_detail.html", context)
