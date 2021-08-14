from django import forms
from .models import Newsletter


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        exclude = (
            'subscription_date',)

        fields = [
            'email',
        ]

        def clean_email(self):
            email = self.cleaned_data.get('email')

            return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'email': 'Email',
        }

        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control border-0 rounded-0 links-text py-2 h-100'
            self.fields[field].label = False
