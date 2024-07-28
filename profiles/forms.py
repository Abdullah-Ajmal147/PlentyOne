from django import forms
from .models import Profile

class UserProfileForm(forms.ModelForm):
    country = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    address = forms.CharField(max_length=255, required=False)
    postal_code = forms.CharField(max_length=20, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['country', 'city', 'state', 'address', 'postal_code', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['country'].initial = self.instance.country
            self.fields['city'].initial = self.instance.city
            self.fields['state'].initial = self.instance.state
            self.fields['address'].initial = self.instance.address
            self.fields['postal_code'].initial = self.instance.postal_code
            self.fields['avatar'].initial = self.instance.avatar

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile
