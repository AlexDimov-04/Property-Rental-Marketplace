from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.SignInView.as_view(), name='sign_in'),
    path('logout/', views.SignOutView.as_view(), name='sign_out'),
]