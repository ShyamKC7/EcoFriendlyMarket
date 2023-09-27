from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages

class ProductView(View):
 def get (self, request):
    clothing = Product.objects.filter(category='C')
    footwear = Product.objects.filter(category='F')
    accessories= Product.objects.filter(category='A')
    fashiontrends = Product.objects.filter(category='FT')
    greengadgets = Product.objects.filter(category='G')
    energyefficientappliances = Product.objects.filter(category='EA')
    return render (request, 'app/home.html', {'clothing': clothing,'footwear': footwear, 'accessories': accessories,'fashiontrends': fashiontrends,'greengadgets': greengadgets, 'energyefficientappliances': energyefficientappliances })
  
 

class ProductDetailView(View):
 def get(self,request,pk):
  product = Product.objects.get(pk=pk)
  return render(request, 'app/productdetail.html',{'product': product})
 
def add_to_cart(request):
 user=request.user
 product_id =request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 7
    total_amount = 0.0
    cart_product = [p for p in cart.objects.all() if p.user ==user]
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount': totalamount, 'amount':amount})


def buy_now(request):
 return render(request, 'app/buynow.html')



def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

def greengadgets(request, data=None):
 if data == None:
  greengadgets = Product.objects.filter(category='G')
 elif data == 'Apple' or data == 'Samsung':
  greengadgets = Product.objects.filter(category='G').filter
  source_function(brand=data)
 return render(request, 'app/greengadgets.html',{'greengadgets': greengadgets})

class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', 
    {'form':form})

 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, "Welcome to EcoFriendlyMarket!Join our green family, shop responsibly, and make the world better one eco-friendly choice at a time. Log in to start your sustainable journey today!")
   form.save()
  return render(request, 'app/customerregistration.html', 
  {'form':form})
  

def checkout(request):
 return render(request, 'app/checkout.html')

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Success! Your profile has been updated. Your eco-friendly journey continues with the latest changes you've made. Thank you for being a part of our sustainable community.")
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
