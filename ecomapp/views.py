from django.shortcuts import render,get_object_or_404, redirect
from django.http import JsonResponse
import json
from django.views.generic import DetailView
from ecomapp import models, utils, signals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage 
from django.conf import settings
from django.template.loader import render_to_string

from django.contrib.contenttypes.models import ContentType

# from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here

def register(req):
    
    if req.POST:
        email = req.POST['email']
        username = req.POST['username']
        password1= req.POST['password1']
        password2= req.POST['password2']
        try:
            x = models.User.objects.get(email=email)
            if x.email == email :
                messages.warning(req,"Email Already taken")
                return redirect('register')
        except:
            pass
        try:
            y = models.User.objects.get(username=username)
            if y.username == username:
                messages.warning(req,"Username already taken")
                return redirect('register')
        except:
            pass   
        if password1 != password2:
            messages.warning(req,"Password Doesn't match")
            return redirect('register')
        models.User.objects.create_user(username=username, email=email, password=password1)
        messages.success(req,"Register successfull")
        return redirect('/')
    return render(req, "register.html")


def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/')
    if request.POST:
        email = request.POST['email']
        password= request.POST['password']
        user = authenticate(email =  email, password = password)
        print(user)
        if user:
            login(request, user)
            request.session.set_expiry(3600) # 1hour 
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
        user = req.user
        try:
            order= models.Cart.objects.get(customer=user, is_completed=False)
        #   items = order.orderitem_set.all()
            cartItem = order.get_item_total
        except:
            pass
            cartItem = 0
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
        user = req.user
        order, created = models.Cart.objects.get_or_create(customer=user, is_completed=False)
        items = order.orderitem_set.all()
        # for i in items:
        #     if i.is_completed == False:
        #         items = models.CartItem.objects.get(id=i.id)
        cartItem = order.get_item_total
        id = order.id
        obj = models.Cart.objects.get(id=id)
        obj.total = order.get_cart_total
        obj.save()
        if order.get_item_total == 0 and order.is_completed == False :
            obj = models.Cart.objects.get(id=id)
            obj.delete()
    else:
        cookiesDatas = utils.cookiesData(req)
        cartItem = cookiesDatas['cartItem'] 
        order = cookiesDatas['orders'] 
        items = cookiesDatas['items'] 

    context = {
        'items': items,
        'orders': order,
        "cartItem": cartItem
    }
    return render(req, 'cart.html', context)

@login_required(login_url='/login')
def check(req):
    if req.user.is_authenticated:
        user = req.user
        order, created = models.Cart.objects.get_or_create(customer=user, is_completed=False)
        items = order.orderitem_set.all()
        cartItem = order.get_item_total
        id = order.id
        if req.POST:
            name = req.POST['name']
            address= req.POST['address']
            city= req.POST['city']
            state= req.POST['state']
            zipcode= req.POST['zipcode']
            country= req.POST['country']
            payment= req.POST['payment']
            obj = models.Cart.objects.get(id=id)
            obj.method = payment
            obj.save()
            ship = models.Shipping.objects.get(customer= req.user)
            if ship == None:
                models.Shipping.objects.create(customer=req.user, address=address, city=city, state=state, zipcode=zipcode, country=country,payment=payment)
            # ship = models.Shipping.objects.get(customer= req.user)
            context = {
                "ship": ship,
                'orders': order,
            }
            return render(req, "checkcontinue.html", context)
        
    else:
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
    
def checkSuccess(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = models.Cart.objects.get_or_create(customer=user, is_completed=False)
        items = order.orderitem_set.all()
        cartItem = order.get_item_total
        ship = models.Shipping.objects.get(customer= request.user)
        ship_id = ship.id
        tot = order.get_cart_total
        method = ship.payment
        id = order.id
        obj = models.Cart.objects.get(id=id)
        obj.is_completed = True
        obj.address = ship
        obj.save()
        
        models.Order.objects.create(cart=order, total =tot, method=method, address=ship)
        # obj = models.CartItem.objects.get(order=id,is_completed=False)
        # print(id)
        # obj.is_completed = True
        # obj.save()
        
        
    else:
        cookiesDatas = utils.cookiesData(request)
        cartItem = cookiesDatas['cartItem'] 
        order = cookiesDatas['orders'] 
        items = cookiesDatas['items'] 
    context = { 
        "cartItem": cartItem,
        "ship": ship,
    }
    return render(request, "checksuccess.html")

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("productId", productId)
    print("action", action)

    user = request.user
    product = models.Product.objects.get(id=productId)
    # x = models.Cart.objects.get(customer=user,is_completed=False)
    # if x.is_completed == False or x == None:
    #     order, created = models.Cart.objects.create(customer=user,is_completed=False)
    # else:
    #     order = models.Cart.objects.get_or_create(customer=user)
    order, created = models.Cart.objects.get_or_create(customer=user,is_completed=False)
    orderItem, created = models.OrderItem.objects.get_or_create(cart=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <=0 :
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

def productView(req, slug):
    if req.user.is_authenticated:
        obj = get_object_or_404(models.Product,slug=slug)
        obj.views = obj.views + 1
        obj.save()
        user = req.user
        order, created = models.Cart.objects.get_or_create(customer=user)
        items = order.orderitem_set.all()
        cartItem = order.get_item_total
        signals.product_viewed_signal.send(obj.__class__, instance=obj, request=req)
    else:
        obj = get_object_or_404(models.Product,slug=slug)
        cookiesDatas = utils.cookiesData(req)
        cartItem = cookiesDatas['cartItem'] 
        order = cookiesDatas['orders'] 
        items = cookiesDatas['items'] 
        
    context = {
        'items': items,
        'orders': order,
        "cartItem": cartItem,
        "product": obj
    }
    return render(req, "product.html", context)

@login_required(login_url='/login')        
def OrderView(request):
    if request.user.is_authenticated:
        user = request.user
        orderimg = models.OrderItem.objects.all()
        orderviews = models.Order.objects.all()
        # order= models.Cart.objects.get(customer=user, is_completed=True)
        # items = order.orderitem_set.all()
        # for i in models.Order.objects.all():
        #     print(i.cart)
        #     for j in models.OrderItem.objects.all():
        #         if i.cart == j.cart:
        try:
            order= models.Cart.objects.get(customer=user, is_completed=False)
            items = order.orderitem_set.all()
            cartItem = order.get_item_total
        except Exception as e:
            pass
            cartItem = 0
            items = {}
            # orderviews = {}
            print("Err", e)
    else:
        cookiesDatas = utils.cookiesData(request)
        cartItem = cookiesDatas['cartItem'] 
        order = cookiesDatas['orders'] 
        items = cookiesDatas['items'] 
    context = { 
        "cartItem": cartItem,
        "orderviews": orderviews,
        "orderimg": orderimg
        
    }
    return render(request, "order.html", context)

# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('change_password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'change.html', {
#         'form': form
#     })

@login_required(login_url='/login')
def change_password(request):
    if request.POST:
        password= request.POST['oldpassword']
        password1= request.POST['password1']
        password2= request.POST['password2']
        if password1 != password2:
            messages.warning(request,"Password Doesn't match")
            return redirect('change_password')
        if password and password1 :
            saveuser = models.User.objects.get(id=request.user.id)
            if saveuser.check_password(password):
                saveuser.set_password(password1)
                saveuser.save()
                update_session_auth_hash(request, saveuser)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('/')
            else:
                messages.warning(request,"Old Password Not match")
                return redirect('change_password')
    
    return render(request, "change.html")


def resetPassword(request):
    if request.POST:
        email= request.POST['email']
        try:
            user = models.User.objects.get(email=email)
            user.is_forget = True
            user.save()
            sendMail(user, request)
            messages.success(request, 'Click the link in the E-Mail')
            print("user", user)
            # uid = urlsafe_base64_encode(force_bytes(user.pk))
            # token = utils.generate_token.make_token(user)
            # # token = RefreshToken.for_user(user).access_token
        except Exception as e:
            print("ssss", e)
    return render(request, "reset.html")

def sendMail(user, request):
    current_site = get_current_site(request)
    email_subject = "Forget password"
    email_body = render_to_string('forget.html' , {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': utils.generate_token.make_token(user),
    })
    email = EmailMessage(subject= email_subject, body=email_body,from_email = settings.EMAIL_HOST_USER,to=[user.email])

    email.send()

def forgetPassword(request, uidb64, token):
    print(request.path)
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = models.User.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user.is_forget == True:
        if request.POST:
            password= request.POST['password1']
            password2= request.POST['password2']
            if password != password2:
                messages.warning(request,"Password Doesn't match")
                # return redirect('/forget-password'+'/'+uidb64+'/'+token)
                return redirect
            if user and utils.generate_token.check_token(user, token):
                # password= request.POST['password1']
                user.set_password(password)
                user.is_forget = False
                user.save()
                messages.success(request, 'Change the password successfull, Please login')
                return redirect('/')
    else:       
        return render(request, "failed.html")

    return render(request, "forgetPassword.html")


def shirt(request):
    category = "Shirt"
    categories = models.Category.objects.filter(name=category)
    product = models.Product.objects.get(category=categories)
    print("categories", categories)
    print("product", product)
    if req.user.is_authenticated:
        user = req.user
        order, created = models.Cart.objects.get_or_create(customer=user)
        items = order.orderitem_set.all()
        cartItem = order.get_item_total
    else:
        cookiesDatas = utils.cookiesData(request)
        cartItem = cookiesDatas['cartItem'] 
        order = cookiesDatas['orders'] 
        items = cookiesDatas['items'] 
    context = { 
        "product": categories,
        "cartItem": cartItem
        
    }
    return render(request, 'shirt.html', context)

@login_required(login_url='/login')
def UserProductHistory(request):
    if request.user.is_authenticated:
        c_type = ContentType.objects.get_for_model(models.Product)
        qs = models.ProductViewed.objects.filter(content_type=c_type, user=request.user)
        context = {
            "qs": qs
        }
        return render(request, 'productview.html', context)
    else:
        messages.warning(request,"Please Login")
        return redirect('/')

