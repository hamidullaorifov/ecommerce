import email
from django import forms
from store.models import Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError 



class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField()
    class Meta:
        model = Customer
        fields = ['name','email','password1','password2']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control',}),
            'password1':forms.PasswordInput(attrs={'class':'form-control',}),
            'password2':forms.PasswordInput(attrs={'class':'form-control',})
        }
    def name_clean(self):  
        name = self.cleaned_data['name'].lower()  
        new = User.objects.filter(username = name)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return name  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['name'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user  




