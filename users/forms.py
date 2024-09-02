from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import CustomUser
from django import forms
from django.contrib.auth import authenticate

# class PhoneLoginForm(AuthenticationForm):
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
#     phone_number = forms.CharField(validators=[phone_regex], max_length=17, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

#     def __init__(self, *args, **kwargs):
#         super(PhoneLoginForm, self).__init__(*args, **kwargs)
#         self.fields['username'] = self.fields.pop('phone_number')  # AuthenticationForm expects 'username'
#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['password'].widget.attrs['class'] = 'form-control'
class PhoneLoginForm(forms.Form):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=17, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        password = cleaned_data.get('password')

        user = CustomUser.objects.filter(phone_number=phone_number).exists()
        # user = authenticate(phone_number=phone_number, password=password)
        if user is None:
            self.add_error(None, 'Invalid phone number or password.')

        return cleaned_data


# class CustomUserCreationForm(UserCreationForm):
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
#     phone_number = forms.CharField(validators=[phone_regex], max_length=17, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
#     invite_code = forms.CharField(max_length=8, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter invite code'}))
#     agreement = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

#     def __init__(self, *args, **kwargs):
#         super(CustomUserCreationForm, self).__init__(*args, **kwargs)
#         self.fields['phone_number'].widget.attrs['class'] = 'form-control'
#         self.fields['password1'].widget.attrs['class'] = 'form-control'
#         self.fields['password2'].widget.attrs['class'] = 'form-control'
#         self.fields['invite_code'].widget.attrs['class'] = 'form-control'
#         self.fields['agreement'].widget.attrs['class'] = 'form-check-input'

#     class Meta:
#         model = CustomUser
#         fields = ('phone_number', 'password1', 'password2', 'invite_code')

#     def clean_agreement(self):
#         agreement = self.cleaned_data.get('agreement')
#         if not agreement:
#             raise forms.ValidationError("You must agree to the Registration Agreement.")
#         return agreement

# class CustomUserCreationForm(forms.ModelForm):
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
#     phone_number = forms.CharField(validators=[phone_regex], max_length=17, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))
#     invite_code = forms.CharField(max_length=8, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter invite code'}))
#     # agreement = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

#     class Meta:
#         model = CustomUser
#         fields = ('phone_number', 'password1', 'password2', 'invite_code')#, 'agreement')

#     def clean(self):
#         cleaned_data = super().clean()
#         phone_number = cleaned_data.get('phone_number')

#         if CustomUser.objects.filter(phone_number=phone_number).exists():
#             self.add_error('phone_number', 'User with this phone number already exists.')

#         password1 = cleaned_data.get('password1')
#         password2 = cleaned_data.get('password2')

#         if password1 and password2 and password1 != password2:
#             self.add_error('password2', "Passwords do not match.")

#         return cleaned_data
    
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_active = False  # Set is_active to False by default

#         if commit:
#             user.set_password(self.cleaned_data['password1'])
#             user.save()

#         return user
class CustomUserCreationForm(forms.ModelForm):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=17, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))
    invite_code = forms.CharField(max_length=8, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter invite code'}))
    # agreement = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'password1', 'password2', 'invite_code')#, 'agreement')

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')

        if CustomUser.objects.filter(phone_number=phone_number).exists():
            self.add_error('phone_number', 'User with this phone number already exists.')

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # Set is_active to False by default

        invite_code = self.cleaned_data.get('invite_code')
        if invite_code:
            user.joining_invitation_code = invite_code

        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.save()

        return user   

class UnifiedUserForm(forms.ModelForm):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=17, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}), required=False)
    invite_code = forms.CharField(max_length=8, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter invite code'}))
    # agreement = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'password1', 'password2', 'invite_code')

    def __init__(self, *args, **kwargs):
        self.is_registration = kwargs.pop('is_registration', True)
        super().__init__(*args, **kwargs)

        if not self.is_registration:
            self.fields.pop('password2')
            self.fields.pop('invite_code')
            self.fields.pop('agreement')
        else:
            self.fields['password2'].required = True

        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs['class'] = 'form-control'
        if 'invite_code' in self.fields:
            self.fields['invite_code'].widget.attrs['class'] = 'form-control'
        if 'agreement' in self.fields:
            self.fields['agreement'].widget.attrs['class'] = 'form-check-input'

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        password = cleaned_data.get('password1')
        print(f"Clean method called, is_registration: {self.is_registration}, phone_number: {phone_number}")

        if self.is_registration:
            if CustomUser.objects.filter(phone_number=phone_number).exists():
                self.add_error('phone_number', 'User with this phone number already exists.')
                print(f"Validation error: User with phone number {phone_number} already exists.")
        else:
            # user = authenticate(phone_number=phone_number, password=password)
            user = CustomUser.objects.filter(phone_number=phone_number).exists()
            if user is None:
                self.add_error(None, 'Invalid phone number or password.')
                print(f"Validation error: Invalid phone number or password for {phone_number}.")

        return cleaned_data

