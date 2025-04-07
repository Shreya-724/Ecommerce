from django.shortcuts import render,HttpResponse,redirect
from .models import Product,Category,Profile
from django.contrib import messages
from django.contrib.auth.models import User
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q





def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')



def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		# Get Current User's Shipping Info
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		if form.is_valid() or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')



def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')










def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        #query
        searched = Product.objects.filter(Q(name__icontains=searched)   |  Q(description__icontains=searched))
        
        if not searched:
         messages.success(request, "that product doesnot exist")
         return render(request, "search.html", {})
        else:
            
     
         return render(request, "search.html", {'searched': searched})
        
    return render(request, 'search.html', {})

    

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
            messages.success(request, ("you have been logged in"))
            return redirect('/home/')
        else:
             messages.success(request, ("there was an error plz try again later")) 
             return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html',{"categories":categories})
        
    

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

