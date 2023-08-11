from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('property_rental_marketplace.profile_management.urls')),
    path('authenticate/', include('property_rental_marketplace.user_authentication.urls')),
    path('properties/', include('property_rental_marketplace.property_market.urls'))
]

handler404 = 'property_rental_marketplace.profile_management.views.custom_404'