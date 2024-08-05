from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout 
from accounts.forms import CustomPasswordChangeForm, PasswordChangeForm, ProfileForm
from orders.models import Layer, WithdrawalRequest
from profiles.models import UserProfile, Profile
from django.conf import settings

@login_required
def setting(request):
    if request.user.is_authenticated:
        user= request.user
        try:
            user_profile = get_object_or_404(UserProfile, user=user)
            try:
                profile = get_object_or_404(Profile, user=user)
                profile = profile.avatar.url
                print('profile', profile)
            except:
                profile = None
                print()
            # layer = Layer.objects.#(id=user_profile.layer_information.id)

            # layer = Layer.objects.all()
            # print('layer', layer)
            context = {
                'current_balance': user_profile.current_balance,
                'amount_frozen': user_profile.amount_frozen,
                'credit': user_profile.credit,
                'invitation_code':user_profile.invitation_code,
                'phone_number':user_profile.phone_number,
                'avatar': profile,
                # 'layer': layer,
                'base_url': settings.BASE_URL,
            }
            return render(request, 'accounts/settings.html', context )
        except Exception as e:
            print(str(e))
            return render(request, 'users/login.html' )
    else:
        return render(request, 'users/login.html')

# def profile_view(request):

#     return render(request, 'accounts/profile.html')

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('plentyone:home')  # Redirect to the profile page or another page
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

def records_view(request):
    return render(request, 'accounts/records.html')

def layer_information_view(request):
    layer = Layer.objects.all()
    context = {
        'layer': layer,
        'base_url': settings.BASE_URL,
    }
    return render(request, 'accounts/layer_information.html', context)

# def change_password_view(request):

#     return render(request, 'accounts/change_password.html')


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(data=request.POST)
        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('plentyone:home')
        else:
            # Print errors to console for debugging
            print(form.errors)
    else:
        form = CustomPasswordChangeForm()

    return render(request, 'accounts/change_password.html', {'form': form})
    

@login_required
def payment_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['new_password']
            print(password)
            user = request.user
            # Assuming the user should have a related WithdrawalRequest object
            withdraw = get_object_or_404(Profile, user=user)
            withdraw.payment_password = password
            withdraw.save()
            messages.success(request, "Password changed successfully")
            return redirect('plentyone:home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm()

    return render(request, 'accounts/payment_password.html', {'form': form})

def terms_and_conditions(request):
    return render(request, 'accounts/terms.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('users:login')  # Redirect to the login page after logout

#Extras
import random
import string

def generate_invitation_code():
    return ''.join(random.choices(string.digits, k=6))

def share_page(request):
    invitation_code = generate_invitation_code()
    return render(request, 'accounts/share.html', {'invitation_code': invitation_code})