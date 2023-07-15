# from property_rental_marketplace.user_authentication.decorators import allowed_users
from property_rental_marketplace.user_authentication.models import UserProfile
from property_rental_marketplace.user_authentication.decorators import unauthenticated_user_restricted
from property_rental_marketplace.user_authentication.forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views
from django.utils.decorators import method_decorator

# 1 week in seconds
SESSION_EXPIRATION_TIME = 604_800

@method_decorator(unauthenticated_user_restricted, name='dispatch')
class RegisterView(views.CreateView):
    template_name = "authentication/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("sign_in")

    def form_valid(self, form):
        checkbox = self.request.POST.get("privacy_policy")

        if not checkbox:
            messages.info(
                self.request, "You must accept the privacy policy to register!"
            )
            return self.render_to_response(self.get_context_data(form=form))

        user = form.save(commit=False)
        user.save()

        user_profile = UserProfile.objects.create(user=user)
        user_profile.first_name = form.cleaned_data['first_name']
        user_profile.last_name = form.cleaned_data['last_name']
        user_profile.save()
        
        messages.success(
            self.request, "User: " + user.username + " successfully created an account!"
        )

        return super().form_valid(form)

@method_decorator(unauthenticated_user_restricted, name='dispatch')
class SignInView(auth_views.LoginView):
    template_name = "authentication/login.html"

    def form_invalid(self, form):
        messages.info(self.request, "Incorrect password or username!")
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if remember_me:
                request.session.set_expiry(SESSION_EXPIRATION_TIME)  

            return super().post(request, *args, **kwargs)
        else:
            messages.info(request, "Incorrect password or username!")
            return render(request, self.template_name)


class SignOutView(auth_views.LogoutView):
    pass
