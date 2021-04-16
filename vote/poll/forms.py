from django import forms
from django.contrib.auth.models import User
from .models import Candidate

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput,
        }



class ChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class CandidateProForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['resume','bio','profile_pic']
        widgets = {
            'bio': forms.Textarea,
        }
