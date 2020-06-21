from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import TrainerProfile
from phone_field import PhoneFormField, PhoneWidget


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email Address')

    class Meta:
        model = User
        fields = '__all__'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group = Group.objects.get(name='Trainers')
        group.user_set.add(self.user)


class ProfileForm(forms.ModelForm):
    image = forms.ImageField(label='Profile Picture')
    city = forms.CharField()
    state = forms.CharField()
    cell = PhoneFormField(label='Phone Number', widget=PhoneWidget)
    facebook = forms.URLField()
    instagram = forms.URLField()
    twitter = forms.URLField()
    linkedin = forms.URLField()
    bio = forms.CharField(label='Biography', widget=forms.Textarea)

    class Meta:
        model = TrainerProfile
        fields = ['image', 'bio', 'city', 'state', 'cell', 'facebook', 'twitter', 'instagram', 'linkedin']


