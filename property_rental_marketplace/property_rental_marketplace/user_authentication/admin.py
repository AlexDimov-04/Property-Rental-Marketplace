from django.contrib import admin
from property_rental_marketplace.user_authentication.models import UserProfile, UserComment, UserPayment

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(UserComment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(UserPayment)
class PaymentAdmin(admin.ModelAdmin):
    pass
