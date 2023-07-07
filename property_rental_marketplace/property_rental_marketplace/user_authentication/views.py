from property_rental_marketplace.user_authentication.decorators import allowed_users
from property_rental_marketplace.user_authentication.decorators import unauthenticated_user_restricted
from property_rental_marketplace.user_authentication.forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views
from django.utils.decorators import method_decorator

# 1 week in seconds
SESSION_EXPIRATION_TIME = 604_800

@login_required(login_url="sign_in")
@allowed_users(allowed_roles=['admin'])
def index(request):
    if request.session.get_expiry_age() == SESSION_EXPIRATION_TIME:
        print(SESSION_EXPIRATION_TIME)
        messages.info(request, "Session has expired. Please log in again.")

    return render(request, "home/index.html")

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
        messages.success(
            self.request, "User: " + user.username + " successfully created an account!"
        )

        return super().form_valid(form)

@method_decorator(unauthenticated_user_restricted, name='dispatch')
class SignInView(auth_views.LoginView):
    template_name = "authentication/login.html"
    next_page = reverse_lazy('index')

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
    next_page = reverse_lazy("sign_in")
