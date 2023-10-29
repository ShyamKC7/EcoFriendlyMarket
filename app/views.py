from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class ProductView(View):
 def get (self, request):
    totalitem = 0
    clothingbrands = Product.objects.filter(category='C')
    footwear = Product.objects.filter(category='F')
    accessories= Product.objects.filter(category='A')
    greengadgets = Product.objects.filter(category='G')
    energyefficientappliances = Product.objects.filter(category='EA')
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
    return render (request, 'app/home.html', {'clothingbrands': clothingbrands,'footwear': footwear, 'accessories': accessories,'greengadgets': greengadgets, 'energyefficientappliances': energyefficientappliances,'totalitem':totalitem})
  
 

class ProductDetailView(View):
 def get(self,request,pk):
  totalitem = 0
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
     totalitem = len(Cart.objects.filter(user=request.user))
     item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request, 'app/productdetail.html',{'product': product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})
 
@login_required 
def add_to_cart(request):
 user=request.user
 product_id =request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 9
        total_amount = 0.0

        # cart_product = [p for p in Cart if p.user == user]
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
        
                totalamount = amount + shipping_amount  # Moved here (same level of indentation)

            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount, 'totalitem':totalitem})
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount = 0.0
    shipping_amount = 9.99
    cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
     
    data= {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount': amount + shipping_amount 

      }
    return JsonResponse(data)
      
def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity-=1
    c.save()
    amount = 0.0
    shipping_amount = 9.99
    cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

    data= {
      'quantity': c.quantity,
      'amount': amount,
      'totalamount': amount + shipping_amount 
      }
    return JsonResponse(data)
  
def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount = 0.0
    shipping_amount = 9.99
    cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount

    data= {
      'amount': amount,
      'totalamount': amount + shipping_amount 
      }
    return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html', {'order_placed': op, 'totalitem':totalitem})



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
  
@login_required
def checkout(request):
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 9.99
  totalamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
  if cart_product:
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
    totalamount = amount + shipping_amount
  return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})

@login_required 
def payment_done(request): 
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user, customer=customer, product= c.product, quantity=c.quantity).save()
    c.delete()
  return redirect("orders")

@method_decorator(login_required, name='dispatch')
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
