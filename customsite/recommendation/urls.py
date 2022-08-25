
from django.urls import path
from . import views

app_name = "Recommendation"

urlpatterns = [
    path('reviews/',views.reviews, name='reviews'),
    path('reviews/product_reviews/<int:id>/',views.product_reviews, name='product_reviews'),
    path('reviews/product_reviews_update/<int:pk>/',views.product_reviews_update, name='product_reviews_update'),
    path('reviews/delete/<int:id>/',views.product_reviews_delete, name='product_reviews_delete'),
    path('reviews_detail/<int:pk>/',views.reviews_detail, name='reviews_detail'),
    path('tag_reviews/',views.tag_reviews, name='tag_reviews'),
    path('tag_reviews_detail/<int:pk>/',views.tag_reviews_detail, name='tag_reviews_detail'),
    path('finished/',views.finished, name='finished'),
    path('finished_detail/<int:pk>/',views.finished_detail, name='finished_detail'),
    path('finished_delete/<int:id>/',views.finished_delete, name='finished_delete'),
]
