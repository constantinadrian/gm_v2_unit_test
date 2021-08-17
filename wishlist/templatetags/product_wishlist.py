from django import template


register = template.Library()


@register.filter(name='check_wishlist')
def check_wishlist(product, wishlist):
    """
    Returns the bool value if product is on wishlist
    """
    if product in wishlist:
        return True
