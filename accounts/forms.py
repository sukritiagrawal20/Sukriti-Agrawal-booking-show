from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "phone", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data.get("phone", "")
            profile.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
