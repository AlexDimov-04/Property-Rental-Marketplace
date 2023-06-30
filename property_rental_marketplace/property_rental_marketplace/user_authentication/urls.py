from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.SignInView.as_view(), name='sign_in'),
    path('logout/', views.logout, name='sign_out')
]