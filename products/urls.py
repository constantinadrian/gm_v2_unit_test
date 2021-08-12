from django.urls import path
from . import views

urlpatterns = [
     path('', views.all_products, name='products'),
     path('add_product/', views.add_product, name="add_product"),
     path('edit_product/<int:product_id>',
          views.edit_product, name="edit_product"),
     path('delete_product/<int:product_id>',
          views.delete_product, name="delete_product"),
     path('add_review/<slug:product_slug>/',
          views.add_review, name="add_review"),
     path('<slug:category_slug>/<slug:product_slug>/', views.product_detail,
          name='product_detail'),
     path('<slug:category_slug>/', views.all_products,
          name='products_from_category'),
]
