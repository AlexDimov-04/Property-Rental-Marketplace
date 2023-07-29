from django.urls import path
from property_rental_marketplace.property_market.views import PropertyListView, PropertyCreateView


urlpatterns = [
    path('list-properties/', PropertyListView.as_view(), name='property_list'),
    path('create-properties/', PropertyCreateView.as_view(), name='property_create'),
]