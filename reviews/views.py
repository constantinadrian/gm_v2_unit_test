from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ReviewForm
from .models import Review
from profiles.models import UserProfile
from products.models import Product


def reviews(request):
    """" A view to return the index page """
    reviews = Review.objects.all()

    context = {
        'reviews': reviews,
    }

    return render(request, "reviews/reviews.html", context)


@login_required
def add_review(request, product_slug):
    """
    Add review to a product to the store
    """
    user = UserProfile.objects.get(user=request.user)
    product = get_object_or_404(Product, slug=product_slug)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = user
            review.product = product
            review.save()

            messages.success(request, (f'Successfully added review '
                                       f'to {product.name}'))
            return redirect(
                reverse('add_review',
                        kwargs={'product_slug': product.slug}))
        else:
            messages.error(request,
                           ('Failed to add review to product. '
                            'Please ensure the form is valid.'))

    else:
        review_form = ReviewForm()

    template = 'reviews/add_review.html'
    context = {
        'product': product,
        'review_form': review_form,
        'product_management': True,
    }

    return render(request, template, context)
