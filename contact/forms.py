from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = (
            'sent_date',)

        fields = [
            'name',
            'email',
            'message'
        ]

        def clean_email(self):
            email = self.clean_email.get('email')

            return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'name': 'Your Name',
            'email': 'Email Address',
            'message': 'Message',
        }

        self.fields['name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0'
            self.fields[field].label = False
