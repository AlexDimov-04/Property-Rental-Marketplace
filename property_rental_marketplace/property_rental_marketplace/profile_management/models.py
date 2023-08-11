from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.subject


class NewsletterFollower(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class AdminNewsLetterPost(models.Model):
    newsletter_type = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="newsletter_images")
    url_redirect = models.URLField()

    def __str__(self):
        return self.content
