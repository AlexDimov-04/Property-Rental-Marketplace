from django.urls import path
from property_rental_marketplace.property_market.views import PropertyListView, PropertyCreateView \
    ,get_additional_form_fields, PropertyDetailsView

urlpatterns = [
    path('list-properties/', PropertyListView.as_view(), name='property_list'),
    path('create-properties/', PropertyCreateView.as_view(), name='property_create'),
    path('get_additional_form_fields/', get_additional_form_fields, name='additional_form_fields'),
    path('property/<int:pk>/', PropertyDetailsView.as_view(), name='property_details')
]