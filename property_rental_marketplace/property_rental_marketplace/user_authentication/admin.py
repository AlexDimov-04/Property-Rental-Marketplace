from django.contrib import admin
from property_rental_marketplace.user_authentication.models import UserProfile

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    pass
