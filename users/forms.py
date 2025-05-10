from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ClientSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.Role.CLIENT
        if commit:
            user.save()
        return user


class PsychologistSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.Role.PSYCHOLOGIST
        if commit:
            user.save()
        return user