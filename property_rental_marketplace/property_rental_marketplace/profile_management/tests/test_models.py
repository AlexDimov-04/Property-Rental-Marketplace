from django.test import TestCase
from property_rental_marketplace.profile_management.models import ContactMessage, NewsletterFollower \
    ,AdminNewsLetterPost


class ContactMessageModelTest(TestCase):
    def test_str_representation(self):
        contact_message = ContactMessage(
            name="John Doe",
            email="john@example.com",
            subject="Test Subject",
            message="Test Message",
        )
        self.assertEqual(str(contact_message), "Test Subject")


class NewsletterFollowerModelTest(TestCase):
    def test_str_representation(self):
        newsletter_follower = NewsletterFollower(email="john@example.com")
        self.assertEqual(str(newsletter_follower), "john@example.com")


class AdminNewsLetterPostModelTest(TestCase):
    def test_str_representation(self):
        admin_newsletter_post = AdminNewsLetterPost(
            newsletter_type="Type A",
            content="Test Content",
            url_redirect="https://example.com",
        )
        self.assertEqual(str(admin_newsletter_post), "Test Content")

    def test_image_upload_path(self):
        admin_newsletter_post = AdminNewsLetterPost.objects.create(
            newsletter_type="Type B",
            content="Test Content",
            url_redirect="https://example.com",
        )
        image_path = admin_newsletter_post.image.path
        self.assertTrue(image_path.startswith("newsletter_images/"))

    def test_image_upload_url(self):
        admin_newsletter_post = AdminNewsLetterPost.objects.create(
            newsletter_type="Type C",
            content="Test Content",
            url_redirect="https://example.com",
        )
        image_url = admin_newsletter_post.image.url
        self.assertTrue(image_url.startswith("/media/newsletter_images/"))
