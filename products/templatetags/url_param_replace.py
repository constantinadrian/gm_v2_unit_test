from django import template


register = template.Library()


# credit code
# https://stackoverflow.com/questions/54808110/django-combining-search-view-with-pagination
@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()
