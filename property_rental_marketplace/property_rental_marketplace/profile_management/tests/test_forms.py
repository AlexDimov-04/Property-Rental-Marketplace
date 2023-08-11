from django.test import TestCase
from property_rental_marketplace.profile_management.forms import UserProfileUpdateForm, ContactForm, NewsLetterSubscriberForm, AdminNewsLetterPostForm


class FormsTestCase(TestCase):
    def test_valid_user_profile_update_form(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
        }
        form = UserProfileUpdateForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_profile_update_form(self):
        data = {
            "first_name": "J",
            "last_name": "Doe123",
            "email": "invalid",
        }
        form = UserProfileUpdateForm(data=data)
        self.assertFalse(form.is_valid())

    def test_contact_form(self):
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Test Subject",
            "message": "Test message content.",
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_newsletter_subscriber_form(self):
        data = {
            "user": None,
        }
        form = NewsLetterSubscriberForm(data=data)
        self.assertTrue(form.is_valid())

    def test_admin_newsletter_post_form(self):
        data = {
            "newsletter_type": "Type",
            "content": "Test content",
            "url_redirect": "http://example.com",
        }
        form = AdminNewsLetterPostForm(data=data)
        self.assertTrue(form.is_valid())

    def test_admin_newsletter_post_form_invalid_url(self):
        data = {
            "newsletter_type": "Type",
            "content": "Test content",
            "url_redirect": "invalid_url",
        }
        form = AdminNewsLetterPostForm(data=data)
        self.assertFalse(form.is_valid())

    def test_admin_newsletter_post_form_empty_content(self):
        data = {
            "newsletter_type": "Type",
            "content": "",
            "url_redirect": "http://example.com",
        }
        form = AdminNewsLetterPostForm(data=data)
        self.assertFalse(form.is_valid())
