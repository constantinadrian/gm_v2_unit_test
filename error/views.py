from django.shortcuts import render


def bad_request_400(request, exception):
    """"
    A view to return 400 bad request page
    Args:
        request : django request object
        exception: django exception object
    Returns:
        rendered 400 html
    """
    return render(request, "error/400.html")


def permission_denied_403(request, exception):
    """"
    A view to return 403 permission denied page
    Args:
        request : django request object
        exception: django exception object
    Returns:
        rendered 403 html
    """
    return render(request, "error/403.html")


def page_not_found_404(request, exception):
    """"
    A view to return 404 page not found
    Args:
        request : django request object
        exception: django exception object
    Returns:
        rendered 404 html
    """
    context = {}
    return render(request, "error/404.html", context)


def internal_server_error_500(request):
    """"
    A view to return 500 internal server error page
    Args:
        request : django request object
    Returns:
        rendered 500 html
    """
    return render(request, "error/500.html")
