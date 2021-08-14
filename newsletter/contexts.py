from .forms import NewsletterForm


def newsletter_form(request):
    """
    Context processor that return
    the newsletter form on all pages
    """
    newsletter_form = NewsletterForm()

    context = {
        "newsletter_form": newsletter_form,
    }

    return context
