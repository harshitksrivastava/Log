from django import forms
from . models import Profile

class NewUserForm(forms.ModelForm):
    password2 = forms.CharField(label='Confirm Password',max_length=8)
    class Meta():
        model = Profile
        fields= ('username','email','password','password2')



class UserForm(forms.Form):
    username = forms.CharField(label='Username',max_length=25)
    password = forms.CharField(label='password',max_length=25)
