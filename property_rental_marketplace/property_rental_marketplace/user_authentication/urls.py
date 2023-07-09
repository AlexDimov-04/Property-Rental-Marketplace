from django.urls import include, path
from . import views
from django_email_verification import urls as mail_urls

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.SignInView.as_view(), name='sign_in'),
    path('logout/', views.SignOutView.as_view(), name='sign_out'),
]