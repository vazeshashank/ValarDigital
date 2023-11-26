from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import auth,User
from django.contrib import messages
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth import get_user_model
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .customAuth import CustomUserAuth
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm
from .models import Products
# Create your views here.


def is_customer(user):
    return user.is_authenticated and user.user_type == 2

def is_vendor(user):
    return user.is_authenticated and user.user_type == 1

User = get_user_model()


def home(request):
    return render(request,'home.html')


def loginPage(request):
    return render(request,'login.html')

def registerPage(request):
    return render(request,'register.html')


    

@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)
def vendReg(request):
    if request.user.is_authenticated:
        return redirect('cusDash')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        if not username:
            messages.info(request, "Username cant be empty")
            return redirect('vendReg')
        if not email:
            messages.info(request, "Password  cant be empty")
            return redirect('vendReg')
        if not password1:
            messages.info(request, "email cant be empty")
            return redirect('vendReg')
        if not password2:
            messages.info(request, "Password  cant be empty")
            return redirect('vendReg')
        if password1 == password2:
            if(User.objects.filter(username=username).exists()):
                messages.info(request,"Username already taken")
                return redirect('vendReg')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,user_type=1)
                user.save()
                return redirect('vendLog')
        else:
            messages.info(request,"Password Mismatch")
            return redirect('vendReg')
    else:
        return render(request,'vendReg.html')
















@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)
def custReg(request):
    if request.user.is_authenticated:
        return redirect('cusDash')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        if not username:
            messages.info(request, "Username cant be empty")
            return redirect('custReg')
        if not email:
            messages.info(request, "Password  cant be empty")
            return redirect('custReg')
        if not password1:
            messages.info(request, "email cant be empty")
            return redirect('custReg')
        if not password2:
            messages.info(request, "Password  cant be empty")
            return redirect('custReg')
        if password1 == password2:
            if(User.objects.filter(username=username).exists()):
                messages.info(request,"Username already taken")
                return redirect('custReg')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,user_type=2)
                user.save()
                return redirect('custLog')
        else:
            messages.info(request,"Password Mismatch")
            return redirect('custReg')
    else:
        return render(request,'custReg.html')

@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)
def logoutPage(request):
    logout(request)
    return redirect('cusDash')



def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.username = request.user
            form.save()
            return redirect('myProds') 
    else:
        form = ProductForm()

    return render(request, 'addProd.html', {'form': form})
















@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)
def vendLog(request):
    # if request.user.is_authenticated:
    #     return redirect('cusDash')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if not username:
            messages.info(request,"Username cant be empty")
            return redirect('vendLog')
        if not password:
            messages.info(request,"Password cannot be empty")
            return redirect('vendLog')
        
        user = CustomUserAuth.custom_authenticate(request,username=username,password=password,user_type=1)
        if user is not None:
            login(request,user)
            print(user.is_authenticated)
            user_type = user.user_type
            return redirect('myProds')
            # return redirect('venDash')   #Vendor pages only
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('vendLog')
    else:
        return render(request, 'vendLog.html')











@cache_control(no_cache=True,must_revalidate=True,no_store=True,max_age=0)
def custLog(request):
    if request.user.is_authenticated:
        return redirect('cusDash')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        
        if not username:
            messages.info(request,"Username cant be empty")
            return redirect('custLog')
        if not password:
            messages.info(request,"Password cannot be empty")
            return redirect('custLog')
        user = CustomUserAuth.custom_authenticate(request,username=username,password=password,user_type=2)
        if user is not None:
            login(request,user)
            user_type = user.user_type
            return redirect(reverse('cusDash'))   #Customer pages only
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('custLog')
    else:
        return render(request, 'custLog.html')
    
@user_passes_test(is_vendor,'vendLog')
def vendor_dashboard(request):
    return render(request, 'venDash.html', {'user_type': 1})


def customer_dashboard(request):
    #filter products by Name or Description
    query = request.GET.get('query')
    if query:
        user_products = Products.objects.filter( item_name__icontains = query) | \
                         Products.objects.filter( brand__icontains = query)
    else:
        allP = Products.objects.all()
        user_products = list(allP.values())
    return render(request, 'cusDash.html', {'products': user_products})


@login_required(login_url='vendLog')
def myProds(request):
    myProds = Products.objects.filter(username=request.user)
    return render(request,'myProds.html',{'myProds': myProds})


@login_required(login_url='custLog')
def add_to_cart(request, product_id):
    
        product = Products.objects.get(pk=product_id)
        cart_item = Products.objects.filter(id=product_id).first()
        if cart_item:
            
            cart_item.quantity += 1
            cart_item.save()
        else:
            # If the product is not in the cart, add it with quantity=1
            product.id = None  # Create a new instance to avoid primary key conflict
            product.user = request.user
            product.quantity = 1
            product.save()
    

        return redirect('cusDash')

@login_required(login_url='vendLog')
def remove_from_cart(request,product_id):
    product = Products.objects.get(pk=product_id)
    product.quantity = 0
    product.save()

    return redirect('view_cart')

@login_required(login_url='vendLog')
def checkout(request):
    # Retrieve products in the user's cart
    cart_products = Products.objects.filter(quantity__gt=0)

    # Mark items as purchased (you might have a 'purchased' field in your model)
    for product in cart_products:
        product.quantity = 0
        product.save()

    return render(request, 'checkout.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='vendLog')
def view_cart(request):
    # Retrieve products in the user's cart
    if request.method == 'POST':
        pass
    cart_products = Products.objects.filter( quantity__gt=0)
    total_price = sum(product.price * product.quantity for product in cart_products)

    return render(request, 'cart.html', {'cart_products': cart_products, 'total_price': total_price})

@login_required(login_url='vendLog')
def delete_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('myProds')  
    return render(request, 'delete.html', {'product': product})

@login_required(login_url='vendLog')
def edit_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('myProds')  # Redirect to the view displaying all products
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})

def test(request):
    return render(request,'test.html')