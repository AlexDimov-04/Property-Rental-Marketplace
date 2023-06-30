from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View 

def index(request):
    return render(request, 'authentication/index.html')

class RegisterView(View):
    template_name = 'authentication/register.html'

    def post(self, request):
        fname = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmed_password = request.POST.get('confirmed_password')

        user = User.objects.create_user(username, email, password)
        user.first_name = fname
        messages.success(request, 'Successful registration!!!')

        return redirect('index')
    
    def get(self, request):
        return render(request, self.template_name)
    

class SignInView(View):
    template_name = 'authentication/login.html'

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        name = user.first_name

        context = {
            'name': name
        }

        if user is None:
            messages.error(request, 'Wrong Credentials! Try again!')
            return redirect('index')
        else:
            login(request, user)
            name = user.first_name

            context = {
                'name': name
            }
            return render(request, 'authentication/index.html', context=context)
        
    def get(self, request):
        return render(request, self.template_name)
    

def logout(request):
    return render(request, 'authentication/logout.html')