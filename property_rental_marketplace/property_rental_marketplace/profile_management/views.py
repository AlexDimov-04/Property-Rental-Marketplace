import requests
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from property_rental_marketplace.profile_management.forms import UserProfileUpdateForm
from property_rental_marketplace.property_market.models import BaseProperty, SavedProperty
from property_rental_marketplace.profile_management.models import (
    ContactMessage,
    NewsletterFollower,
    AdminNewsLetterPost,
)
from property_rental_marketplace.profile_management.forms import (
    ContactForm,
    NewsLetterSubscriberForm,
    AdminNewsLetterPostForm,
)
from property_rental_marketplace.profile_management.signals import (
    send_notification_to_followers,
)
from property_rental_marketplace.user_authentication.forms import UserCommentForm
from property_rental_marketplace.user_authentication.models import (
    UserProfile,
    UserComment,
)
from django.db.models import Count
from django.core.mail import EmailMessage
from django.db import transaction


class UserProfileMixin:
    def get_user_profile(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            try:
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                user_profile = None
            return user_profile

        return None


class IndexView(UserProfileMixin, views.TemplateView):
    template_name = "hero_page/landing_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = self.get_user_profile()
        context["comments"] = UserComment.objects.all()

        property_counts = BaseProperty.objects.values("property_type").annotate(
            count=Count("property_type")
        )

        property_type_counts = {}
        for item in property_counts:
            property_type_counts[item["property_type"]] = item["count"]

        context["property_type_counts"] = property_type_counts

        return context


class AboutView(UserProfileMixin, views.CreateView):
    model = AdminNewsLetterPost
    template_name = "about_page/about.html"
    form_class = AdminNewsLetterPostForm
    success_url = reverse_lazy("about")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = self.get_user_profile()
        context["newsletter_posts"] = AdminNewsLetterPost.objects.all()

        return context

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        send_notification_to_followers(sender=self.model, instance=self.object)
        return response


class ContactsView(UserProfileMixin, views.CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = "contacts/contacts.html"
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = self.get_user_profile()

        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        message = form.cleaned_data["message"]

        email_subject = f"Message Title: {subject}"
        email_body = f"Name: {name}\nEmail: {email}\nMessage:\n {message}"
        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            to=["rentwise.marketplace@gmail.com"],
            reply_to=[email],
        )
        email.send()

        messages.success(self.request, "Your message has been sent successfully!")

        return response


class NewsLetterView(UserProfileMixin, views.FormView):
    template_name = "newsletter/newsletter_subscribe.html"
    model = NewsletterFollower
    form_class = NewsLetterSubscriberForm
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_email = self.request.user.email
        context["user_profile"] = self.get_user_profile()
        context["is_subscribed"] = self.model.objects.filter(email=user_email).exists()

        return context

    def form_valid(self, form):
        user_email = self.request.user.email
        is_subscribed = self.model.objects.filter(email=user_email).exists()

        if is_subscribed:
            self.model.objects.filter(email=user_email).delete()
            messages.success(self.request, "You have been unsubscribed.")
        else:
            subscriber, created = self.model.objects.get_or_create(email=user_email)
            if created:
                messages.success(
                    self.request, "You have successfully subscribed to our newsletter."
                )

        return super().form_valid(form)


class FaqView(UserProfileMixin, views.TemplateView):
    template_name = "faq/faq.html"


class SavedPropertiesCollectionView(LoginRequiredMixin, UserProfileMixin, views.ListView):
    model = SavedProperty
    template_name = "properties/saved_properties_collection.html"
    context_object_name = "saved_properties"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = self.get_user_profile()

        return context


class UserCommentView(LoginRequiredMixin, UserProfileMixin, views.FormView):
    template_name = "comments/comments.html"
    form_class = UserCommentForm
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = self.get_user_profile()

        return context

    def form_valid(self, form):
        user_profile = UserProfile.objects.get(user=self.request.user)
        form.instance.user_profile = user_profile
        form.save()

        messages.success(self.request, "You left a comment successfully.")

        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, UserProfileMixin, views.DetailView):
    model = UserProfile
    template_name = "profiles/profile_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()

        context["user_profile"] = self.get_user_profile()
        context["first_name"] = user_profile.first_name
        context["last_name"] = user_profile.last_name
        context["birth_date"] = user_profile.birth_date
        context["email"] = user_profile.email
        context["gender"] = user_profile.gender
        context["country"] = user_profile.country
        context["phone"] = user_profile.phone
        context["profile_image"] = user_profile.profile_image
        context["bio"] = user_profile.bio
        context["countries"] = get_countries()

        return context

    def get_object(self):
        return self.request.user.userprofile


class UserProfileUpdateView(LoginRequiredMixin, UserProfileMixin, views.UpdateView):
    model = UserProfile
    form_class = UserProfileUpdateForm
    template_name = "profiles/profile_update.html"
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()

        context["user_profile"] = self.get_user_profile()
        context["gender_choices"] = UserProfile.GENDER_CHOICES
        context["gender"] = user_profile.gender
        context["countries"] = get_countries()
        context["country"] = user_profile.country

        return context

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def form_valid(self, form):
        user = self.request.user

        email = form.cleaned_data.get("email")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")

        if email:
            user.email = email

        user.first_name = first_name if first_name else ""
        user.last_name = last_name if last_name else ""

        user.save()

        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Profile update failed. Please correct the errors."
        )
        return super().form_invalid(form)


class UserProfileDeleteView(LoginRequiredMixin, UserProfileMixin, views.DeleteView):
    model = UserProfile
    template_name = "profiles/profile_delete.html"
    success_url = reverse_lazy("sign_out")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = self.get_user_profile()
        return context

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Profile deleted successfully.")
        return super().delete(request, *args, **kwargs)


@staticmethod
def get_countries():
    try:
        response = requests.get("https://restcountries.com/v2/all")
        response.raise_for_status()

        countries = response.json()
        return countries
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve countries: {e}")

    return []


def custom_404(request, exception):
    return render(request, "404 error/404.html", status=404)
