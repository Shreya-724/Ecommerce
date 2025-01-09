from django.shortcuts import render,redirect
from .models import Product,Category
from django.contrib import messages


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

