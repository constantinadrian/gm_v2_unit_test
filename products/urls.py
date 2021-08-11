from django.urls import path
from . import views

urlpatterns = [
     path('', views.all_products, name='products'),
     path('add_product/', views.add_product, name="add_product"),
     path('<slug:category_slug>/<slug:product_slug>/', views.product_detail,
          name='product_detail'),
     path('<slug:category_slug>/', views.all_products,
          name='products_from_category'),
]
