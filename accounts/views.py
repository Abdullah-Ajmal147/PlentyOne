from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout 

def settings(request):
    return render(request, 'accounts/settings.html')

def profile_view(request):
    return render(request, 'accounts/profile.html')

def records_view(request):
    return render(request, 'accounts/records.html')

def layer_information_view(request):
    return render(request, 'accounts/layer_information.html')

def change_password_view(request):
    return render(request, 'accounts/change_password.html')

def payment_password_view(request):
    return render(request, 'accounts/payment_password.html')

def terms_and_conditions(request):
    return render(request, 'accounts/terms.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')  # Redirect to the login page after logout

#Extras
import random
import string

def generate_invitation_code():
    return ''.join(random.choices(string.digits, k=6))

def share_page(request):
    invitation_code = generate_invitation_code()
    return render(request, 'accounts/share.html', {'invitation_code': invitation_code})