from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class sign_form(UserCreationForm):
    email = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Use a list to maintain order
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'class': 'form-control'}),
        }



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    # Optional: Customize the form fields if needed
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
