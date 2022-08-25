from unicodedata import name
from django.urls import path
from . import views

app_name = "Order"

urlpatterns = [
    path('order/', views.order, name="order"),
    path('order/delete/', views.order_delete, name="order_delete"),
    path('order/order_des/',views.order_des, name="order_des"),
    path('order/order_des/custom1/',views.custom1, name="custom1"),
    path('order/order_des/custom2',views.custom2, name="custom2"),
    path('order/order_des/customend', views.customend, name="customend"),
    path('payment/', views.payment,name="payment"),
    path('loading/', views.loading, name="loading"),
    path('loading2/', views.loading2, name="loading2"),
    path('kakaoPayLogic/', views.kakaoPayLogic, name="kakaoPayLogic"),
    path('paySuccess/', views.paySuccess, name="paySuccess"),
    
]
