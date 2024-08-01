from django import forms
from orders.models import WithdrawalRequest

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['amount', 'network', 'address', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Amount'})
        self.fields['network'].widget.attrs.update({'class': 'form-select', 'placeholder': 'Select crypto'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Address'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your withdrawal password'})
