from django.shortcuts import render,get_object_or_404, redirect
from django.http import JsonResponse
import json
from django.views.generic import DetailView
from ecomapp import models, utils, forms

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def register(req):
    if req.POST:
        email = req.POST['email']
        username = req.POST['username']
        password1= req.POST['password1']
        password2= req.POST['password2']
        try:
            x = models.User1.objects.get(email=email)
        
            if x.email == email :
                messages.warning(req,"Already taken")
                return redirect('register')
        except:
            pass
        if password1 != password2:
            messages.warning(req,"Password Doesn't match")
            return redirect('register')
        models.User1.objects.create_user(username=username, email=email, password=password1)
        return redirect('/')
    return render(req, "register.html")


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/')
    if request.POST:
        email = request.POST['email']
        password= request.POST['password']
        # user = authenticate(email =  email, password = password)
        user = authenticate(email =  email, password = password)
        print(user)
        if user:
            login(request, user)
            return redirect('/')
        if not authenticate(email =  email, password = password):
            messages.warning(request,"Invalid Login")
            return redirect('login')
    return render(request, 'login.html')
def logout_view(request):
    logout(request)
    return redirect('/')


def index(req):
    product = models.Product.objects.all()
    if req.user.is_authenticated:
        # print(req.user.user)
        user = req.user
        order, created = models.Order.objects.get_or_create(customer=user)
        items = order.orderitem_set.all()
        cartItem = order.get_item_total
    else:
        # items = []
        # order = { 'get_cart_total': 0, 'get_item_total': 0}
        # cartItem = order['get_item_total']
        cookiesDatas = utils.cookiesData(req)
        cartItem = cookiesDatas['cartItem'] 
        order = cookiesDatas['orders'] 
        items = cookiesDatas['items'] 
    context = { 
        "product": product,
        "cartItem": cartItem
        
    }
    return render(req, 'store.html', context)

def cart(req):
    if req.user.is_authenticated:
        # print(req.user.user)
        user = req.user
        order, created = models.Order.objects.get_or_create(customer=user)
        items = order.orderitem_set.all()
        cartItem = order.get_item_total
    else:
        cookiesDatas = utils.cookiesData(req)
        cartItem = cookiesDatas['cartItem'] 
        order = cookiesDatas['orders'] 
        items = cookiesDatas['items'] 
        # cart = json.loads(req.COOKIES['cart'])
        # print('cart', cart)
        
    context = {
        'items': items,
        'orders': order,
        "cartItem": cartItem
    }
    return render(req, 'cart.html', context)

def check(req):
    if req.user.is_authenticated:
        # print(req.user.user)
        user = req.user
        order, created = models.Order.objects.get_or_create(customer=user)
        items = order.orderitem_set.all()
        cartItem = order.get_item_total
        
    else:
        # items = []
        # order = { 'get_cart_total': 0, 'get_item_total': 0}
        # cartItem = order['get_item_total']
        cookiesDatas = utils.cookiesData(req)
        cartItem = cookiesDatas['cartItem'] 
        order = cookiesDatas['orders'] 
        items = cookiesDatas['items'] 
    context = {
        'items': items,
        'orders': order,
        "cartItem": cartItem
    }
    return render(req, 'check.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("productId", productId)
    print("action", action)

    user = request.user
    product = models.Product.objects.get(id=productId)
    order, created = models.Order.objects.get_or_create(customer=user)
    orderItem, created = models.OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <=0 :
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

def productView(req, slug):
    # productId = req.GET.get()
    # obj = models.Product.objects.all()
    # obj = get_object_or_404(models.Product,slug=slug)
    if req.user.is_authenticated:
        # print(req.user.user)
        obj = get_object_or_404(models.Product,slug=slug)
        user = req.user
        order, created = models.Order.objects.get_or_create(customer=user)
        items = order.orderitem_set.all()
        cartItem = order.get_item_total
    else:
        obj = get_object_or_404(models.Product,slug=slug)
        cookiesDatas = utils.cookiesData(req)
        cartItem = cookiesDatas['cartItem'] 
        order = cookiesDatas['orders'] 
        items = cookiesDatas['items'] 
        # cart = json.loads(req.COOKIES['cart'])
        # print('cart', cart)
        
    context = {
        'items': items,
        'orders': order,
        "cartItem": cartItem,
        "product": obj
    }
    # context = {
    #     "product": obj
    # }
    return render(req, "product.html", context)
# class view(DetailView):
#     model = models.Product
#     template_name = "view.html"
#     def get(self):
        

def checkbox(req):
    if req.method == "GET":
        name = req.GET.get('name', True)
        print(name)
    return render(req, "checkbox.html")

