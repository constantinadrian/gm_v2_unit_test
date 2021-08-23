from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    """
    Model that stores a category,
    related to :model:`products.category`
    """

    class Meta:
        verbose_name_plural = "Categories"

    parent = models.ForeignKey('self', related_name='child',
                               null=True, blank=True,
                               on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254, unique=True, null=False)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_friendly_name(self):
        return self.friendly_name

    def get_absolute_url(self):
        return reverse(
            'products_from_category',
            kwargs={'category_slug': self.slug}
        )


class Product(models.Model):
    """
    Model that stores a product,
    related to :model:`products.category`
    """

    class Meta:
        verbose_name_plural = 'Products'

    CODE_FIELDS_SIZE = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
    )

    sku = models.CharField(max_length=254, null=True, blank=True)
    brand = models.CharField(max_length=254)
    name = models.CharField(max_length=254)
    slug = models.SlugField(max_length=254, unique=True, null=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey("Category", null=True, blank=True,
                                 on_delete=models.SET_NULL)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    has_sizes = models.BooleanField(default=False)
    fields_size = models.IntegerField(default=0, choices=CODE_FIELDS_SIZE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'product_detail',
            kwargs={'category_slug': self.category.slug,
                    'product_slug': self.slug}
        )
