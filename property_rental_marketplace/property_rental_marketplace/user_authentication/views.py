from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from property_rental_marketplace.user_authentication.forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# 1 week in seconds
SESSION_EXPIRATION_TIME = 604800

@login_required(login_url="sign_in")
def index(request):
    if request.session.get_expiry_age() == SESSION_EXPIRATION_TIME:
        messages.info(request, "Session has expired. Please log in again.")

    return render(request, "home/index.html")


class RegisterView(View):
    template_name = "authentication/register.html"

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        checkbox = request.POST.get("privacy_policy")

        if form.is_valid():
            if not checkbox:
                messages.info(
                    request, "You must accept the privacy policy to register!"
                )
                return render(request, self.template_name, {"form": form})

            user = form.save(commit=False)
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]

            messages.success(
                request, "User: " + user.username + " successfully created an account!"
            )
            user.save()

            return redirect("sign_in")

        return render(request, self.template_name, {"form": form})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")

        form = UserRegistrationForm()

        for field in form.fields.values():
            field.error_messages = {}

        return render(request, self.template_name, {"form": form})


class SignInView(View):
    template_name = "authentication/login.html"

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if remember_me:
                request.session.set_expiry(SESSION_EXPIRATION_TIME)  

            return redirect("index")
        else:
            messages.info(request, "Incorrect password or username!")
            return render(request, self.template_name)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")

        return render(request, self.template_name)


def sign_out(request):
    logout(request)
    return redirect("sign_in")
