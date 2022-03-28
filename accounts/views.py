from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from store.models import Customer
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from random import randint




# Create your views here.



def register(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        name = request.POST['name']
        username=to_username(name)
        if User.objects.filter(email=email).exists():
            return render(request,'accounts/register.html')
        if password1==password2 and password1 and name and email:
            user = User.objects.create_user(username,email,password1)
            customer = Customer.objects.create(user=user,name=name)
            customer.save()
            login(request,user)
            return redirect('/')
            # else:
            #     raise ValidationError('Password doesn\'t match')
    return render(request,'accounts/register.html')


def loginview(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        print(password)
        if User.objects.filter(email=email).exists():
            customeruser = User.objects.get(email=email)
            user = authenticate(request,username=customeruser.username,password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            
        
        # user = authenticate(request,email=email,password=password)
        
            
    return render(request,'accounts/login.html')


def to_username(s):
    parts = s.lower().split()
    username = ''
    for item in parts:
        username+=item
    while User.objects.filter(username=username).exists():
        username+=str(randint(0,10))
    return username
