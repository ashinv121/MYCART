from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from home.form import CustomUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
# Create your views here.
def home(request):
    product=Product.objects.filter(tending=1)
    return render(request, "shop/index.html",{"trending_product":product})

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=="POST":
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Sucessfully.")
                return redirect("/")
            else:
                messages.error(request, "Invalid User Name or Password!")
                return redirect("/login")
        return render(request, "shop/login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout Sucessfully.")
        return redirect("/")
    
"""def add_to_cart(request):
    #print ("hai")
    #print( JsonResponse({'status':'Invalid Access'}, status=400))
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
       if request.user.is_authenticated:
           data=json.load(request)
           product_id=data['pid']
           product_qty=data['product_qty']
           product_status=Product.objects.get(id=product_id)
           if product_status:
               #print("1")
               cart_status=Cart.objects.get(user=request.user.id, product_id=product_id)
              # print("2")
               if cart_status:
                    if cart_status.product_qty == product_qty:
                        return JsonResponse({'status':'Product alredy in Cart'}, status=200)
                        
                    else:
                         cart_item=Cart.objects.get(user=request.user, product_id=product_id,)
                         cart_item.product_qty = product_qty
                         cart_item.save()
                         return JsonResponse({'status':'Product Quantity updated '}, status=200)
        
               else:
                   if product_status.quantity>=product_qty:
                       Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                       return JsonResponse({'status':'Product addeed Sucessfully'}, status=200)
                   else:
                       return JsonResponse({'status':'Product is out off stock'}, status=200)                  
           #print(request.user.id)
           #print( JsonResponse({'status':'Invalid Access'}, status=400))
           #return JsonResponse({'status':'Product addeed Sucessfully'}, status=200)
       else:           
           #print( JsonResponse({'status':'Invalid Access'}, status=400))
           return JsonResponse({'status':'Please Login'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=400)
    # if request.user.is_authenticated:
    #     logout(request)
    #     messages.success(request, "Logout Sucessfully.")
    #     return redirect("/")    

 """
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)


            product_id = data['pid']
            product_qty = data['product_qty']
            product_status = Product.objects.get(id=product_id)
            print(product_id)

            if product_status:
                try:
                    cart_item = Cart.objects.get(user=request.user, product_id=product_id)
                    if cart_item.product_qty == product_qty:
                        return JsonResponse({'status': 'Product already in Cart'}, status=200)
                    else:
                        cart_item.product_qty = product_qty
                        cart_item.save()
                        return JsonResponse({'status': 'Product Quantity updated'}, status=200)
                except Cart.DoesNotExist:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                        return JsonResponse({'status': 'Product added Successfully'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product is out of stock'}, status=200)
            else:

                return JsonResponse({'status': 'Invalid Product ID'}, status=400)
        else:           
            return JsonResponse({'status': 'Please Login'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)
   
def favorite(request):
    #print ("hai")
    #print( JsonResponse({'status':'Invalid Access'}, status=400))
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
       if request.user.is_authenticated:
           data=json.load(request)
           product_id=data['pid']
           product_status=Product.objects.get(id=product_id)
           if product_status:               
               if Favorite.objects.filter(user=request.user.id, product_id=product_id):
                    #Favorite.objects.delete(user=request.user, product_id=product_id)

                    favorite_to_delete = Favorite.objects.filter(user=request.user, product_id=product_id)
                    favorite_to_delete.delete()
                    return JsonResponse({'status':'Product removed from Wishlist'}, status=200)
               else:
                    Favorite.objects.create(user=request.user, product_id=product_id, favorite=True)
                    return JsonResponse({'status':'Product Added to Wishlist'}, status=200)
       else:           
           return JsonResponse({'status':'Please Login'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=400)
    
def register(request):
        if request.user.is_authenticated:
            return redirect("/")
        else:

            form=CustomUserForm()
            if request.method=='POST':
                form=CustomUserForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Registration Sucess You Can Login Now")
                    return redirect("/login")

        return render(request, "shop/register.html", {"form":form})

def collections(request):
    catagory=Catogory.objects.filter(status=0)
    return render(request, "shop/collections.html", {"catagory":catagory})


def collectionsview(request, name):
    try:
      catogory = Catogory.objects.get(name=name, status=0)
      products = Product.objects.filter(catogory=catogory)
      return render(request, "shop/products/index.html", {"products": products, "catogory_name":catogory})
    except Catogory.DoesNotExist:
        messages.warning(request, "No Such Category Found")
        return redirect('collections')
    
def product_details(request, cname, pname):
    #print(f'Category Name: {cname}, Product Name: {pname}')
    try:
        category = Catogory.objects.get(name=cname, status=0)
        product = Product.objects.get(name=pname, status=0)
        if request.user.is_authenticated:
          #print("test1")
          try:
               fav = Favorite.objects.get(user=request.user.id, product_id=product.id)
               #print(fav)
          except Favorite.DoesNotExist:
                print("test2")
                fav = None
            
          return render(request, "shop/products/product_details.html", {"product": product, "fav": fav})
        else:
          return render(request, "shop/products/product_details.html", {"product": product})

    except Catogory.DoesNotExist:
        messages.warning(request, "No Such Category Found")
        return redirect('collections')

    except Product.DoesNotExist:
        messages.warning(request, "No Such Product Found")
        return redirect('collections')


def cart(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user.id,)
        return render(request, "shop/cart.html",{"cart":cart})    
    else:
        return redirect("/")
    
       






