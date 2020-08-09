from django import forms
from django.contrib.auth import get_user_model
User=get_user_model()
class ContactForm(forms.Form):
    fullname= forms.CharField(max_length=100)
    email=forms.EmailField( )
    content=forms.CharField(widget=forms.Textarea(attrs={"placeholder":"your contact"}))



    def clean_email(self):
        email=self.cleaned_data['email']
        if not 'gmail.com' in email:
            raise forms.ValidationError("email has to be gmail")
        return email


class GuestForm(forms.Form):
    email=forms.EmailField()

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())
    

class RegisterForm(forms.Form):
    username=forms.CharField()
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput())
    password2=forms.CharField(label = "confirm password",widget=forms.PasswordInput())

    def clean_username(self):
        username=self.cleaned_data['username']
        qs=User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username is taken")
        return username
        
    def clean_email(self):
        email=self.cleaned_data['email']
        qs=User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        data=self.cleaned_data
        password=self.cleaned_data['password']
        password2=self.cleaned_data['password2']
        if password2 != password:
            raise forms.ValidationError("password must match")
        return data
