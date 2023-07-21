from django.urls import path
from property_rental_marketplace.property_market.views import PropertyListView, PropertyCreateView


urlpatterns = [
    path('property-list/', PropertyListView.as_view(), name='property_list'),
    path('property-create/', PropertyCreateView.as_view(), name='property_create'),
]