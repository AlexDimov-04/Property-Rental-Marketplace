from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from property_rental_marketplace.profile_management.models import (
    NewsletterFollower,
    AdminNewsLetterPost,
)


@receiver(post_save, sender=AdminNewsLetterPost)
def send_notification_to_followers(sender, instance, **kwargs):
    followers = NewsletterFollower.objects.all()
    subject = "New Newsletter Post!"
    message = f"A new newsletter post has been published: {instance.content}. Check it out on {settings.REDIRECT_DOMAIN}/about/#newsfeed"
    from_email = "rentwise.marketplace.gmail.com"

    for follower in followers:
        send_mail(subject, message, from_email, [follower.email])
