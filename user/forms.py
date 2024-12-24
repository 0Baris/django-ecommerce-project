from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'E-Posta adresinizi girin', 'required': 'required'}), label="E-Posta")
    name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Adınızı girin', 'required': 'required'}), label="Ad")
    surname = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Soyadınızı girin', 'required': 'required'}), label="Soyad")
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Şifrenizi girin', 'required': 'required'}), label="Şifre")
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Şifrenizi tekrar girin', 'required': 'required'}), label="Şifre Tekrar")

    class Meta:
        model = get_user_model()
        fields = ('name', 'surname', 'email', 'password1', 'password2')