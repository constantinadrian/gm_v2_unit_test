from .models import Product, Category


def new_arrival(request):
    """ Context processor to access all items from new_arrival category """
    new_arrival = Product.objects.all().filter(category__name="new_arrival")

    context = {
        "new_arrival": new_arrival,
    }

    return context


def now_on_sale(request):
    """ Context processor to access all items from sale category """
    now_on_sale = Product.objects.all().filter(category__name="sale")

    context = {
        "now_on_sale": now_on_sale,
    }

    return context


def nav_categories(request):
    """ Context processor for categories for navigation menu """
    nav_categories = Category.objects.filter(parent=None)

    context = {
        "nav_categories": nav_categories,
    }

    return context
