from django import forms
from django.contrib.auth.models import User
from wordgame.models import UserProfile
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    username = forms.CharField(min_length=4, max_length=12, widget=forms.TextInput(
      attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput())
    ConfirmPassword  = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('PasswordConfirm'):
            raise ValidationError('Password confirmation does not match password!')
        else:
            return self.cleaned_data
