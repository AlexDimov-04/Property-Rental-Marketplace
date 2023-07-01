from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from property_rental_marketplace.user_authentication.forms import UserRegistrationForm 
from django.contrib import messages
from django.contrib.auth.decorators import login_required 

@login_required(login_url='sign_in')
def index(request):
    return render(request, 'home/index.html')

class RegisterView(View):
    template_name = 'authentication/register.html'

    def post(self, request):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']

            messages.success(request, 'User: ' + user.username + ' successfully created account!')
            user.save()

            return redirect('sign_in')
    
        return render(request, self.template_name, {'form': form})
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        
        form = UserRegistrationForm()

        for field in form.fields.values():
            field.error_messages = {}

        return render(request, self.template_name, {'form': form})
    
class SignInView(View):
    template_name = 'authentication/login.html'

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.info(request, 'Incorrect password or username!')
            return render(request, self.template_name)
            
        login(request, user)
        return redirect('index')
        
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, self.template_name)
    
def sign_out(request):
    logout(request)
    return redirect('sign_in')