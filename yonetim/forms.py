# yonetim/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Sakin

class UserRegisterForm(forms.ModelForm):
    # Django'nun yerleşik kullanıcı modeli alanları
    username = forms.CharField(label='Kullanıcı Adı')
    email = forms.EmailField(label='E-posta')
    password = forms.CharField(label='Şifre', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Şifre Tekrar', widget=forms.PasswordInput)

    # Sakin profil modeli alanları
    telefon = forms.CharField(label='Telefon Numarası', required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def clean_password2(self):
        # Şifrelerin eşleştiğini kontrol etme
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Şifreler eşleşmiyor.')
        return cd['password2']