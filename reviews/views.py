from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.functions import Lower
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ReviewForm
from .models import Review
from profiles.models import UserProfile
from products.models import Product


def reviews(request):
    """"
    A view to return the reviews page
    Args:
        request : django request object
    Returns:
        rendered reviews html
    """
    reviews = Review.objects.all().order_by('-date_posted')

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

    # Pagination show 12 products per page
    paginator = Paginator(reviews, 12)

    page = request.GET.get('page')
    try:
        all_reviews = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        all_reviews = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_reviews = paginator.page(paginator.num_pages)

    # Pagination was inspired, modified and
    # adapted to this project from from this
    # # Credit code
    # https://www.youtube.com/watch?v=MAIFJ3_bcCY
    index = all_reviews.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'reviews': all_reviews,
        'page_range': page_range,
        'current_sorting': current_sorting,
    }

    return render(request, "reviews/reviews.html", context)


@login_required
def add_review(request, product_slug):
    """
    A view to add review to a product to the store
    Args:
        request : django request object
        product_slug : slug is the part of the URL that is unique
                       for each and every page of a website which
                       identifies a particular product
    Returns:
        rendered add_review html
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
    }

    return render(request, template, context)


@login_required
def edit_review(request, review_id):
    """
    A view to edit a review from a specific product
    Args:
        request : django request object
        product_id : slug is the part of the URL that is unique
                     for each and every page of a website which
                     identifies a particular product id
    Returns:
        rendered edit_review html
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
    }

    return render(request, template, context)


@login_required
def delete_review(request, review_id):
    """
    a view to delete a review from a specific product
    Args:
        request : django request object
        product_id : slug is the part of the URL that is unique
                     for each and every page of a website which
                     identifies a particular product id
    Returns:
        redirect reverse reviews
    """
    # check if review exists
    review = get_object_or_404(Review, pk=review_id)

    # check is there is a userprofile attach to that review
    user = get_object_or_404(UserProfile, pk=review.user.id)

    # check is requested user is the owner of the rewiev
    if not request.user.id == user.id:
        messages.error(request, 'Sorry, only the owner can delete his review.')
        return redirect(reverse('home'))

    review.delete()
    messages.success(request, 'Review deleted!')

    return redirect(reverse('reviews'))
