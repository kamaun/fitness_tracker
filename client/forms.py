from django import forms
from .models import ClientProfile
from phone_field import PhoneFormField, PhoneWidget
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email Address')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group = Group.objects.get(name='Clients')
        group.user_set.add(self.user)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    age = forms.IntegerField()
    cell = PhoneFormField(widget=PhoneWidget)
    trainer = forms.ModelChoiceField(label='Personal Trainer')
    image = forms.ImageField(label='Profile Picture')
    bio = forms.CharField(label='Biography', widget=forms.Textarea)

    class Meta:
        model = ClientProfile
        fields = ['image', 'bio', 'cell', 'trainer']
