from django import forms
from django.contrib.auth.models import User
from wordgame.models import UserProfile
from django.core.exceptions import ValidationError
from django.forms import widgets


class UserForm(forms.ModelForm):
    username = forms.CharField(min_length=4, max_length=12, widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    PasswordConfirm  = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('PasswordConfirm'):
            raise ValidationError('Password confirmation does not match password!')
        else:
            return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    SEX_CHOICES = (
        (0, 'man'),
        (1, 'woman'),
    )
    sex = forms.ChoiceField(choices=SEX_CHOICES, required=False)
    photo = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'email', 'sex', 'photo', 'password')
        widgets = {
            'password': widgets.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['email'].required = False

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists() and self.instance.username != self.cleaned_data['username']:
            raise ValidationError('Username exist')
        return self.cleaned_data['username']
