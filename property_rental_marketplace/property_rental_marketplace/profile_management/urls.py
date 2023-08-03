from django.urls import path, include
from property_rental_marketplace.property_market.views import PropertyListView
from . import views

profile_denpendencies = [
    path('details/', views.UserProfileView.as_view(), name='profile_details'),
    path('update/', views.UserProfileUpdateView.as_view(), name='update_profile'),
    path('delete/', views.UserProfileDeleteView.as_view(), name='delete_profile')
]

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('properties/list_properties/<str:property_type>/', PropertyListView.as_view(), name='list_properties'),
    path('profile/', include(profile_denpendencies)),
]