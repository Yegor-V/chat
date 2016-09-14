from django import forms
from chat_app.models import Credential


class RegistrationForm(forms.ModelForm):
    # name = forms.CharField(max_length=Credential.max_len_users)
    # surname = forms.CharField(max_length=Credential.max_len_users)
    # login = forms.CharField(max_length=Credential.max_len_cred)
    # password = forms.CharField(max_length=Credential.max_len_cred, widget=forms.PasswordInput)
    class Meta:
        model = Credential
        fields = ['name', 'surname', 'login', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class LoginForm(forms.Form):
    login = forms.CharField(max_length=Credential.max_len_cred, label='Login')
    password = forms.CharField(max_length=Credential.max_len_cred, widget=forms.PasswordInput)
