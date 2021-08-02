from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail,
         name='product_detail'),
]
