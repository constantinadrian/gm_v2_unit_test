from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import ContactForm
from profiles.models import UserProfile


def contact(request):
    """"
    A view to return the contact page
    """

    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            if request.user.is_authenticated:
                contact = contact_form.save(commit=False)
                # get the user profile
                profile = UserProfile.objects.get(user=request.user)

                # Attach the user's profile to the contact query
                contact.user_profile = profile
                contact.save()
            else:
                contact_form.save()

            name = contact_form.cleaned_data.get('name')
            email = contact_form.cleaned_data.get('email')
            query = contact_form.cleaned_data.get('subject')
            message = contact_form.cleaned_data.get('message')

            subject = render_to_string(
                'contact/contact_email/contact_email_subject.txt',
                {'query': query})
            body = render_to_string(
                'contact/contact_email/contact_email_body.txt',
                {'message': message, 'email': email, 'name': name})

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False
            )

            messages.success(request, ('Your message has been received. \
                                       Thank you'))
            return redirect(reverse('contact'))
        else:
            messages.error(request,
                           ('Failed to add review to product. '
                            'Please ensure the form is valid.'))
            contact_form = ContactForm()

    else:
        contact_form = ContactForm()

    template = 'contact/contact.html'
    context = {
        'contact_form': contact_form,
    }

    return render(request, template, context)
