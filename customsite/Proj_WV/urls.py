from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('whitevalley/', include('shop.urls')),
    path('whitevalley/user/', include('user.urls')),
    path('whitevalley/magazine/', include('user.urls')),
    path('whitevalley/shopping/', include('order.urls')),
    path('whitevalley/shopping/', include('recommendation.urls')),
    path('whitevalley/cs/', include('cs.urls')),
]
