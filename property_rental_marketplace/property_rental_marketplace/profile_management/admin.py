from django.contrib import admin
from property_rental_marketplace.settings import AWS_S3_CUSTOM_DOMAIN

class CustomAdminSite(admin.AdminSite):
    static_url = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
