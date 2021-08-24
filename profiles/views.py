from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order


@login_required
def profile(request):
    """
    A view to display the user's profile.
    Args:
        request : django request object
    Returns:
        rendered profile html
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request,
                           ('Update failed. Please ensure the form is valid.'))
    else:
        form = UserProfileForm(instance=profile)

    # return the order related to the profile
    orders = profile.orders.all()

    # return all the query that the user has
    queries = profile.userquery.all()

    # populate the form with the user profile current information
    form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'queries': queries,
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    """
    A view to display the user's individual order.
    Args:
        request : django request object
        order_number : unique string which identifies
                       a particular order number
    Returns:
        rendered checkout_success html
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
