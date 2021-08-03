from .models import Product


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
