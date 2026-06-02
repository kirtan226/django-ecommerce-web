from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm ,UsernameField , PasswordChangeForm , PasswordResetForm , SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta(User):
        model = User
        fields = ['username' ,'email' , 'password1','password2']
        labels = {'email':'EMail'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    username = UsernameField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'autocomplete': 'email',
            'class': 'form-control',
            'placeholder': 'Enter your email',
        })
    )
    password = forms.CharField(label=_("Password"),strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            'class': 'form-control',
            'placeholder': 'Enter your password',
        }))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            user = User.objects.filter(email__iexact=email).first()
            if user is None:
                raise self.get_invalid_login_error()

            self.user_cache = authenticate(
                self.request,
                username=user.get_username(),
                password=password,
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class MypasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                                                            'autofocus': True,
                                                                            'class': 'form-control'}))

    new_password1 = forms.CharField(label=_("New Password"),strip=False,
                                    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                                                             'class': 'form-control'}),help_text=password_validation.password_validators_help_text_html())

    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class': 'form-control'}))

class MypasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"),max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email" , 'class': 'form-control'}))

class MysetpasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class': 'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms. CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class' : 'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','state','zipcode']
        widgets = {'name' : forms .TextInput(attrs={'class': 'form-control'}),
                    'locality': forms.TextInput(attrs={'class': 'form-control'}),
                    'city': forms.TextInput(attrs={'class' : 'form-control'}),
                    'state': forms.Select(attrs={'class' : 'form-control'}),
                    'zipcode' : forms.NumberInput(attrs={'class':'form-control'} )}
