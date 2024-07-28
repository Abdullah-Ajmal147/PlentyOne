from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from .models import Profile


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form})



import random
import string

def generate_invitation_code():
    return ''.join(random.choices(string.digits, k=6))

def share_page(request):
    invitation_code = generate_invitation_code()
    return render(request, 'accounts/share.html', {'invitation_code': invitation_code})