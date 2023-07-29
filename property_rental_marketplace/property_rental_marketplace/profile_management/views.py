import requests
from ssl import SSLError
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from property_rental_marketplace.profile_management.forms import UserProfileUpdateForm
from property_rental_marketplace.user_authentication.models import UserProfile

# not for production, it should be changed
@staticmethod
def get_countries():
    try:
        response = requests.get("https://restcountries.com/v2/all", verify=False)
        if response.status_code == 200:
            countries = response.json()
            return countries
    except SSLError as e:
        print(f"Failed to retrieve countries: {e}")
    
    return []

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
        context['user_profile'] = self.get_user_profile()
        return context
    
class UserProfileView(LoginRequiredMixin, UserProfileMixin, views.DetailView):
    model = UserProfile
    template_name = 'profiles/profile_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()

        context['user_profile'] = self.get_user_profile()
        context['first_name'] = user_profile.first_name
        context['last_name'] = user_profile.last_name
        context['birth_date'] = user_profile.birth_date
        context['gender'] = user_profile.gender
        context['gender'] = user_profile.gender
        context['country'] = user_profile.country
        context['bio'] = user_profile.bio
        context['countries'] = get_countries()

        return context

    def get_object(self):
        return self.request.user.userprofile

class UserProfileUpdateView(LoginRequiredMixin, UserProfileMixin, views.UpdateView):
    model = UserProfile
    form_class = UserProfileUpdateForm
    template_name = 'profiles/profile_update.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()

        context['user_profile'] = self.get_user_profile()
        context['gender_choices'] = UserProfile.GENDER_CHOICES
        context['gender'] = user_profile.gender
        context['countries'] = get_countries()
        context['country'] = user_profile.country

        return context

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Profile update failed. Please correct the errors.')
        return super().form_invalid(form)

class UserProfileDeleteView(LoginRequiredMixin, UserProfileMixin, views.DeleteView):
    model = UserProfile
    template_name = 'profiles/profile_delete.html'
    success_url = reverse_lazy('sign_out')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.get_user_profile()
        return context

    def get_object(self, queryset=None):
        return self.request.user.userprofile
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Profile deleted successfully.')
        return super().delete(request, *args, **kwargs)
