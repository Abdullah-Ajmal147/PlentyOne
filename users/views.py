from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from users.models import CustomUser
from .forms import CustomUserCreationForm, PhoneLoginForm
from django.contrib.auth.decorators import login_required
from django.views import View
from users.backends import PhoneNumberBackend
from django.contrib.auth import get_backends


class RegisterView(View):
    form_class = CustomUserCreationForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()

            # Get the backend and set it on the user object
            backends = get_backends()
            if backends:
                user.backend = backends[0].__class__.__module__ + '.' + backends[0].__class__.__name__

            login(request, user, backend=user.backend)
            return redirect('plentyone:home') 
        return render(request, self.template_name, {'form': form})

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class(initial=self.initial)
    #     return render(request, self.template_name, {'form': form})

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         login(request, user)
    #         return redirect('plentyone:home') 
    #     return render(request, self.template_name, {'form': form})

class LoginView(View):
    """
    Handles user login functionality.
    Renders a login form on GET requests and processes the form on POST requests.
    If the form is valid and the user is authenticated, the user is logged in and redirected to the home page.
    """

    form_class = PhoneLoginForm
    initial = {'key': 'value'}
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        """
        Renders the login form.
        """
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """
        Processes the login form, authenticates the user, and logs them in if credentials are valid.
        """
        form = self.form_class(data=request.POST)
        if form.is_valid():
            phone_number=form.cleaned_data.get('phone_number')
            password=form.cleaned_data.get('password')

            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('plentyone:home') 
            else:
                # Invalid login credentials
                form.add_error(None, "Invalid phone number or password.")
                
            # user_obj = CustomUser.objects.filter(phone_number=phone_number).exists()
            # user_obj = PhoneNumberBackend.authenticate(phone_number=phone_number, password=password)
            # if user_obj:
            #     user = CustomUser.objects.get(phone_number=phone_number)
            # else:
            #     print('user not found')
            # # user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            # if user is not None:
            #     login(request, user)
            #     return redirect('plentyone:home') 
        return render(request, self.template_name, {'form': form})
    
    # def post(self, request, *args, **kwargs):
    #     form = PhoneLoginForm(request.POST)
    #     if form.is_valid():
    #         phone_number = form.cleaned_data['phone_number']
    #         password = form.cleaned_data['password']
    #         user = authenticate(request, phone_number=phone_number, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect('home')  # Redirect to the desired page after login
    #         else:
    #             form.add_error(None, 'Invalid phone number or password.')
    #     else:
    #         form = PhoneLoginForm()
    #     return render(request, 'users/login.html', {'form': form})

@login_required
def share(request):
    invitation_code = request.user.invitation_code
    return render(request, 'users/share.html', {'invitation_code': invitation_code})

def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UnifiedUserForm
from .models import CustomUser

def user_view(request):
    is_registration = 'register' in request.path
    print(f"Request method: {request.method}, is_registration: {is_registration}")

    if request.method == 'POST':
        form = UnifiedUserForm(request.POST, is_registration=is_registration)
        print(f"Form valid: {form.is_valid()}, form errors: {form.errors}")

        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password1']

            if is_registration:
                print(f"Checking if user with phone number {phone_number} exists")
                if CustomUser.objects.filter(phone_number=phone_number).exists():
                    form.add_error('phone_number', 'User with this phone number already exists.')
                    print(f"User with phone number {phone_number} already exists")
                else:
                    user = CustomUser.objects.create_user(phone_number=phone_number, password=password)
                    login(request, user)
                    print(f"New user created and logged in with phone number {phone_number}")
                    return redirect('home')  # Redirect to the desired page after registration
            else:
                # user = authenticate(request, phone_number=phone_number, password=password)
                print('phone ------>', phone_number)
                user = CustomUser.objects.filter(phone_number=phone_number).exists()
                print(f"Authenticated user: {user}")
                if user is not None:
                    login(request, user)
                    print(f"User logged in with phone number {phone_number}")
                    return redirect('home')  # Redirect to the desired page after login
                else:
                    form.add_error(None, 'Invalid phone number or password.')
                    print(f"Invalid login attempt for phone number {phone_number}")
    else:
        form = UnifiedUserForm(is_registration=is_registration)

    return render(request, 'users/user_form.html', {'form': form, 'is_registration': is_registration})
