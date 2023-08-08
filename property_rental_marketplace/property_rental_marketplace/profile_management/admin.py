from django.contrib import admin
from property_rental_marketplace.profile_management.models import AdminNewsLetterPost \
,NewsletterFollower, AdminNewsLetterPost, ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    pass

@admin.register(NewsletterFollower)
class NewsletterFollowerAdmin(admin.ModelAdmin):
    pass

@admin.register(AdminNewsLetterPost)
class AdminNewsLetterPostAdmin(admin.ModelAdmin):
    pass