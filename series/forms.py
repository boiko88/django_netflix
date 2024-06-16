from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Anime


class AnimeForm(forms.ModelForm):
    class Meta:
        model = Anime
        fields = ['eng_name', 'director_name', 'release_year', 'episodes_number', 'is_based_on_manga']

    def save(self, commit=True, request=None):
        anime = super().save(commit=False)
        if request:
            anime.user = request.user
        if commit:
            anime.save()
        return anime


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class SignInForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password')
