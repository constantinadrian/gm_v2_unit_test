from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.functions import Lower

from .forms import ReviewForm
from .models import Review
from profiles.models import UserProfile
from products.models import Product


def reviews(request):
    """" A view to return the index page """
    reviews = Review.objects.all()

    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey

            if sortkey == "name":
                sortkey = "lower_name"
                reviews = reviews.annotate(lower_name=Lower('product'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == "desc":
                    sortkey = f'-{sortkey}'

            reviews = reviews.order_by(sortkey)

    current_sorting = f'{sort}_{direction}'

    context = {
        'reviews': reviews,
        'current_sorting': current_sorting
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


@login_required
def edit_review(request, review_id):
    """ Edit a review from a specific product """
    # check if review exists
    review = get_object_or_404(Review, pk=review_id)

    # check is there is a userprofile attach to that review
    user = get_object_or_404(UserProfile, pk=review.user.id)

    # check is the product still exist in db
    product = get_object_or_404(Product, pk=review.product.id)

    # check is requested user is the owner of the rewiev
    if not request.user.id == user.id:
        messages.error(request, 'Sorry, this review does not belong to you.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = user
            review.product = product
            review.save()

            messages.success(request, (f'Successfully updated review '
                                       f'to {product.name}'))
            return redirect(
                reverse('product_detail',
                        kwargs={'category_slug': product.category.slug,
                                'product_slug': product.slug}))
        else:
            messages.error(request,
                           ('Failed to update review to product. '
                            'Please ensure the form is valid.'))

    else:
        review_form = ReviewForm(instance=review)
        messages.info(request, f'You are editing {product.name} review.')

    template = 'reviews/edit_review.html'
    context = {
        'review': review,
        'review_form': review_form,
        'product_management': True,
    }

    return render(request, template, context)


@login_required
def delete_review(request, review_id):
    """
    Delete a review from a specific product
    """
    # check if review exists
    review = get_object_or_404(Review, pk=review_id)

    # check is there is a userprofile attach to that review
    user = get_object_or_404(UserProfile, pk=review.user.id)

    # check is the product still exist in db
    product = get_object_or_404(Product, pk=review.product.id)

    # check is requested user is the owner of the rewiev
    if not request.user.id == user.id:
        messages.error(request, 'Sorry, this review does not belong to you.')
        return redirect(reverse('home'))

    review.delete()
    messages.success(request, 'Review deleted!')

    return redirect(reverse('reviews'))