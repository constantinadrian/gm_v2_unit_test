from django import forms
from .models import Product, Category
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image',
                             required=False,
                             widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()

        # show only the subcategories and
        # categories that don't have parent/child relation
        # in our case exclude from list the follow category:
        # #### Suits
        # #### Formal
        # #### Accesories
        # #### Special Offers
        # Note: For test a new category was added that was not
        #       a child or a parent for any of other category
        #       to see if it shows
        friendly_names = []
        for c in categories:
            parent_category = False
            if c.parent is None:
                for d in categories:
                    if str(c.name) == str(d.parent):
                        parent_category = True
                        break
            if parent_category is False:
                friendly_names.append((c.id, c.get_friendly_name()))

        self.fields['category'].choices = friendly_names

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
