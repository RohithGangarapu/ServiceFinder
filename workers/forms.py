from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    role = forms.ChoiceField(choices=[('customer', 'Customer'), ('worker', 'Worker')])
    profession = forms.CharField(max_length=100, required=False)  # Only for workers

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'role', 'profession', 'password1', 'password2']