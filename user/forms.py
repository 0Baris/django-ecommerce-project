from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Address

## Kullanıcı oluşturma formu.
class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'E-Posta adresinizi girin', 'required': 'required'}), label="E-Posta")
    phone = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Telefon numaranızı girin', 'required': 'required'}), label="Telefon")
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

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.surname = self.cleaned_data['surname']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user

## Kullanıcı ADRES oluşturma formu.
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['title', 'address', 'city', 'district', 'postal_code', 'phone_number']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Başlık'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adres', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Şehir'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'İlçe'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Posta Kodu'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Telefon Numarası'}),
        }
