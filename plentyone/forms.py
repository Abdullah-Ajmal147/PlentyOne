from django import forms
from django.core.exceptions import ValidationError
from profiles.models import Profile
from orders.models import WithdrawalRequest

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['amount', 'network', 'address', 'password']

    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs and pop it
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Amount'})
        self.fields['network'].widget.attrs.update({'class': 'form-select', 'placeholder': 'Select crypto'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Address'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your withdrawal password'})

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if self.user is None:
            raise ValidationError("User is not set.")
        
        user_profile = Profile.objects.get(user=self.user)  # Use the user from kwargs

        if password != user_profile.payment_password:
            print('ppppppp')
            raise ValidationError("The provided password does not match our records.")
        
        return password