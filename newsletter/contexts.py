from .forms import NewsletterForm


def newsletter_form(request):
    """
    Context processor for the
    newsletter form on all pages
    Args:
        request : django request object
    Returns:
        context
    """
    newsletter_form = NewsletterForm()

    context = {
        "newsletter_form": newsletter_form,
    }

    return context
