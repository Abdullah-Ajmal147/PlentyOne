from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from profiles.models import UserProfile, Profile

class CustomPasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}),
        label='New Password'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}),
        label='Confirm New Password'
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")

        password_validation.validate_password(password1)
        return password2
    
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['country', 'city', 'state', 'address', 'postal_code', 'avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'multiple': False}),
        }
