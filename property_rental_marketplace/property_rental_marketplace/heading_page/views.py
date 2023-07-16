from django.shortcuts import render
import requests
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from property_rental_marketplace.heading_page.forms import UserProfileUpdateForm
from property_rental_marketplace.user_authentication.models import UserProfile

@staticmethod
def get_countries():
    url = 'https://restcountries.com/v2/all'
    response = requests.get(url)
    if response.status_code == 200:
        countries = response.json()
        return countries
    else:
        return []

@method_decorator(login_required(login_url="sign_in"), name='dispatch')
class IndexView(views.TemplateView):
    template_name = "hero_page/landing_page.html"

class UserProfileView(LoginRequiredMixin, views.DetailView):
    model = UserProfile
    template_name = 'profiles/profile_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()

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

class UserProfileUpdateView(LoginRequiredMixin, views.UpdateView):
    model = UserProfile
    form_class = UserProfileUpdateForm
    template_name = 'profiles/profile_update.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()

        context['gender'] = user_profile.gender
        context['gender_choices'] = UserProfile.GENDER_CHOICES
        context['countries'] = get_countries()
        context['country'] = user_profile.country

        return context

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def form_valid(self, form):
        if self.request.method == 'POST':
            return render(self.request, 'profiles/profile_popup_window.html')
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Profile update failed. Please correct the errors.')
        return super().form_invalid(form)
          