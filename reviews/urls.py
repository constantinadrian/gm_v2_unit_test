from django.urls import path
from . import views

urlpatterns = [
     path('', views.reviews, name='reviews'),
     path('add_review/<slug:product_slug>/',
          views.add_review, name="add_review"),
     path('edit_review/<int:review_id>',
          views.edit_review, name="edit_review"),
     path('delete_review/<int:review_id>',
          views.delete_review, name="delete_review"),
]
