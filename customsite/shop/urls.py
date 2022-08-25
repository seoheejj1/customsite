from django.urls import path
from . import views

app_name = "Main"

urlpatterns = [
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('cart/<int:id>/', views.cart_number, name="cart_number"),
    path('cart/checked/<int:id>/', views.cart_checked, name="cart_checked"),
    path('cart/delete/<int:id>/', views.cart_delete, name="cart_delete"),
    path('admin/', views.admin, name="admin"),
    path('admin/member/', views.admin_member, name="admin_member"),
    path('admin/member/delete/<int:id>/', views.member_delete, name="member_delete"),
    path('admin/point/', views.admin_point, name="admin_point"),
    path('admin/account/', views.admin_account, name="admin_account"),
    path('admin/account/add/', views.account_add, name="account_add"),
    path('admin/account/delete/<str:bank>/', views.account_delete, name="account_delete"),
]
