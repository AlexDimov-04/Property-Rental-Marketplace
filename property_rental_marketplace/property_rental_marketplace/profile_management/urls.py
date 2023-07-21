from django.urls import path, include
from . import views

profile_denpendencies = [
    path('details/', views.UserProfileView.as_view(), name='profile_details'),
    path('update/', views.UserProfileUpdateView.as_view(), name='update_profile'),
    path('delete/', views.UserProfileDeleteView.as_view(), name='delete_profile')
]

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/', include(profile_denpendencies)),
]