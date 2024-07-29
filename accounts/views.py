from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout 
from orders.models import Layer
from profiles.models import UserProfile

@login_required
def settings(request):
    if request.user.is_authenticated:
        user= request.user
        try:
            user_profile = get_object_or_404(UserProfile, user=user)
            print('user_profile', user_profile)
            # layer = Layer.objects.#(id=user_profile.layer_information.id)

            # layer = Layer.objects.all()
            # print('layer', layer)
            context = {
                'current_balance': user_profile.current_balance,
                'amount_frozen': user_profile.amount_frozen,
                'credit': user_profile.credit,
                'invitation_code':user_profile.invitation_code,
                'phone_number':user_profile.phone_number
                # 'layer': layer,
                # 'base_url': settings.BASE_URL,
            }
            return render(request, 'accounts/settings.html', context )
        except:
            return render(request, 'users/login.html' )
    else:
        return render(request, 'users/login.html')

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