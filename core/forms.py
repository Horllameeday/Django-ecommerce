from django import forms
from django.contrib.auth.models import User

PAYMENT_CHOICES = (
    ('C', 'Cash on Delivery'),
    ('P', 'Pay Now')
)

class OptionForm(forms.Form):
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class CashCheckoutForm(forms.Form):
    address = forms.CharField()
    phone_number = forms.CharField()

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']