from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from .models import Profile, Skill, Message


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'SnowDen'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ulugbek'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Umaraliyev'})
        self.fields['email'].widget.attrs.update({'placeholder': 'example@gmail.com'})
        self.fields['password1'].widget.attrs.update({'placeholder': '********'})
        self.fields['password2'].widget.attrs.update({'placeholder': '********'})
        for key, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input-text'})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'id', 'created']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input input--text'})


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Python'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Something about your work experince with this skill ...'})
        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'input input--text'})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['fullname', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


