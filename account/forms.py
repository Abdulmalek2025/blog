from django import forms
from django.contrib.auth.models import User
from .models import Profile
class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(label="password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="repeate password",widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username','email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password dont mach')
        return cd['password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('job','picture','description',)
