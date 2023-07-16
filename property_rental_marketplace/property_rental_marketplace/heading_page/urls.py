from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile-details/', views.UserProfileView.as_view(), name='profile_details'),
    path('update-profile/', views.UserProfileUpdateView.as_view(), name='update_profile'),
]