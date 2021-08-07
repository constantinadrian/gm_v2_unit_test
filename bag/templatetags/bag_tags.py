from django import template


register = template.Library()


@register.filter(name='split')
def split(value, arg):
    """
    Returns the string into a list of substrings
    separated by the delimiter string.
    """
    return value.split(arg)


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    Returns total price for each product accordingly
    to the quantity. Filter copy from the Boutique Ado project
    """
    return price * quantity
