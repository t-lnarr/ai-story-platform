from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Parola doğrulama mesajlarını özelleştir
        self.fields['password1'].help_text = "Parolanız en az 4 karakter olmalı."
        self.fields['password2'].help_text = "Yukarıdaki parolayı tekrar girin."
        # Varsayılan doğrulayıcıları kaldır
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 4:
            raise forms.ValidationError("Parola en az 4 karakter olmalı.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parolalar eşleşmiyor.")
        return password2
