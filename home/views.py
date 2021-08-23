from django.shortcuts import render


def index(request):
    """"
    A view to return the index page
    Args:
        request : django request object
    Returns:
        rendered index html
    """
    return render(request, "home/index.html")
