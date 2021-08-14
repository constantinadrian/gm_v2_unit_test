from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import NewsletterForm
from .models import Newsletter


def newsletter_signup(request):
    """"
    A view that handles the subscriptions
    """
    if request.method == "POST":
        reddirect_url = request.POST.get('redirect_url')
        subscription_form = NewsletterForm(request.POST)

        if subscription_form.is_valid():
            form = subscription_form.save(commit=False)

            if Newsletter.objects.filter(email=form.email).exists():
                messages.info(request, ('This email address is already '
                                        'subscribed to our newsletter.'))
                return redirect(reddirect_url)
            else:
                form.save()

                email = subscription_form.cleaned_data.get('email')

                subject = render_to_string(
                    'newsletter/newsletter_email/newsletter_email_subject.txt')
                body = render_to_string(
                    'newsletter/newsletter_email/newsletter_email_body.txt',
                    {'email': email})

                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False
                )

                messages.success(request,
                                 (f'Thank you. You are now subscribed '
                                  f'to our newsletter. A confirmation '
                                  f'email will be sent to {email}.'))
                return redirect(reddirect_url)
        else:
            messages.error(request,
                           ('Please ensure the email '
                            'address on the form is valid.'))
            return redirect(reddirect_url)
