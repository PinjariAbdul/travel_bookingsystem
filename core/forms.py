from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Booking

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileUpdateForm(UserChangeForm):
    password = None  # Hide password field
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class BookingForm(forms.Form):
    seats = forms.IntegerField(min_value=1, label='Number of Seats', widget=forms.NumberInput(attrs={
        'class': 'form-control',
    }))

    def __init__(self, *args, **kwargs):
        self.max_seats = kwargs.pop('max_seats', 1)
        super().__init__(*args, **kwargs)
        self.fields['seats'].widget.attrs['max'] = self.max_seats

    def clean_seats(self):
        seats = self.cleaned_data.get('seats')
        if seats > self.max_seats:
            raise forms.ValidationError(f'You can book up to {self.max_seats} seats only.')
        return seats
