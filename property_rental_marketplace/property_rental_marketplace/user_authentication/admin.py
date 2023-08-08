from django.contrib import admin
from property_rental_marketplace.user_authentication.models import UserProfile, UserComment

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(UserComment)
class CommentAdmin(admin.ModelAdmin):
    pass
