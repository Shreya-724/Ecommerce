from django.shortcuts import render,HttpResponse,redirect
from .models import Product,Category
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('/home/')
        else:
             return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def category(request, foo):
    # replace hyphen with spaces
    foo = foo.replace('_', ' ')
    #url bata category grab gareko
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html',{'products':products, 'category':category})
        
    except:
        messages.success(request,("that category deoesnot exist"))
        return redirect('home')
    
    
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html',{'product':product})
    
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})

def about(request):
    return render(request, 'about.html',{})

