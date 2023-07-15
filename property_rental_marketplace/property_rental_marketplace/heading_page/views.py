import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin
from property_rental_marketplace.user_authentication.models import UserProfile

# 1 week in seconds
SESSION_EXPIRATION_TIME = 604_800

def get_countries():
    url = 'https://restcountries.com/v2/all'
    response = requests.get(url)
    if response.status_code == 200:
        countries = response.json()
        return countries
    else:
        return []

class IndexView(views.TemplateView):
    template_name = "hero_page/landing_page.html"

    @method_decorator(login_required(login_url="sign_in"))
    def dispatch(self, request, *args, **kwargs):
        if request.session.get_expiry_age() == SESSION_EXPIRATION_TIME:
            messages.info(request, "Session has expired. Please log in again.")
            
        return super().dispatch(request, *args, **kwargs)

class UserProfileView(LoginRequiredMixin, views.DetailView):
    model = UserProfile
    template_name = 'profiles/profile_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        context['first_name'] = user_profile.first_name
        context['last_name'] = user_profile.last_name
        context['birth_date'] = user_profile.birth_date
        context['gender_choices'] = UserProfile.GENDER_CHOICES
        context['profile_image'] = user_profile.profile_image
        context['countries'] = get_countries()
        return context

    def get_object(self):
        return self.request.user.userprofile
    