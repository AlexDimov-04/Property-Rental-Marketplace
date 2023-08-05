from django.urls import path, include
from property_rental_marketplace.property_market.views import PropertyListView, PropertyCreateView \
    ,get_additional_form_fields, PropertyDetailsView, PropertyUpdateView, PropertyDeleteView \
    ,SavePropertyView, UnsavePropertyView
from django.conf import settings
from django.conf.urls.static import static

properties_operations = [
    path('', PropertyDetailsView.as_view(), name='property_details'),
    path('update/', PropertyUpdateView.as_view(), name='property_update'),
    path('delete/', PropertyDeleteView.as_view(), name='property_delete')
]

urlpatterns = [
    path('list-properties/', PropertyListView.as_view(), name='property_list'),
    path('create-properties/', PropertyCreateView.as_view(), name='property_create'),
    path('get_additional_form_fields/', get_additional_form_fields, name='additional_form_fields'),
    path('save-property/<int:pk>/', SavePropertyView.as_view(), name='save_property'),
    path('unsave-property/<int:pk>/', UnsavePropertyView.as_view(), name='unsave_property'),
    path('property/<int:pk>/', include(properties_operations))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)