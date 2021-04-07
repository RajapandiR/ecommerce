from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from ecomapp import models

class AuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = models.User1
        fields = ('email','password')
    def clean(self):
        email = self.cleaned_data['email']
        print(email)
        password = self.cleaned_data['password']
        print(password)
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid Login")
