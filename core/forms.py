from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

PAYMENT_CHOICES = (
    ('C', 'Cash on Delivery'),
    ('P', 'Pickup')
)

class OptionForm(forms.Form):
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class CashCheckoutForm(forms.Form):
    address = forms.CharField()
    phone_number = forms.CharField()

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')