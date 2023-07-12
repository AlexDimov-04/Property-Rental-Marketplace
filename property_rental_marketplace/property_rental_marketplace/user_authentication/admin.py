from django.contrib import admin
from property_rental_marketplace.user_authentication.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
