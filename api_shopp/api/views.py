import json
import itertools
from django.contrib import messages
from math import ceil
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from .forms import UserRegisterForm, SellerRegisterForm, CustomerRegisterForm
from rest_framework import viewsets
from .serializers import ProductSerializer, OrdersSerializer, LoginSerializer
from .models import Product, Orders, Seller, Customer,OrderUpdate
from django.http import HttpResponse
from django.core.mail import send_mail


# Rest API

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('product_name')
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all().order_by('name')
    serializer_class = OrdersSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('username')
    serializer_class = LoginSerializer


# Views


# 1. Regsitrations


def register_seller(request):
    if request.method == 'POST':
        seller_creds = {
            'username': request.POST.get('username'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
        }
        user = User.objects.create_user(**seller_creds)
        seller = Seller(user=user, company_name=request.POST.get('company_name'))
        seller.save()
        return redirect('user_login')
    else:
        user_register_form = UserRegisterForm()
        seller_register_form = SellerRegisterForm()
    return render(request, 'registration/sellerregd.html',
    {
        'user_register_form': user_register_form,
        'seller_register_form': seller_register_form
    })


def user_register(request):
    if request.method == 'POST':
        customer_creds = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'username': request.POST.get('username')
        }
        user = User.objects.create_user(**customer_creds)
        customer = Customer(user=user, contact=request.POST.get('contact'))
        customer.save()
        return redirect('user_login')
    else:
        user_register_form = UserRegisterForm()
        Customer_register_form = CustomerRegisterForm()
    return render(request, 'registration/registration.html', {
        'user_register_form': user_register_form,
        'Customer_register_form': Customer_register_form
    })

# 2. Login Page


def seller_login(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            # Success, now let's login the user.
            return sellerindex(request)
        else:
            # Incorrect credentials, let's throw an error to the screen.

            return render(request, 'registration/sellerlogin.html',
                          {'error_message': 'Incorrect username and / or password.'})
    else:

        return render(request, 'registration/sellerlogin.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return index(request)
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'registration/login.html',
                          {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data available, let's just show the page to the user.
        return render(request, 'registration/login.html')
# HomePage


@login_required()
def index(request):
    customers = Customer.objects.all()
    cust_usernames = [customer.user.username for customer in customers]
    print(cust_usernames)
    for i in cust_usernames:
        if (i == request.user.username):
            allProds = []
            catprods = Product.objects.values('category', 'id')
            cats = {item['category'] for item in catprods}
            for cat in cats:
                prod = Product.objects.filter(category=cat)
                n = len(prod)
                nSlides = n // 4 + ceil((n / 4) - (n // 4))
                allProds.append([prod, range(1, nSlides), nSlides])

            params = {'allProds': allProds}
            return render(request, 'shopp/index.html', params)
        else:
            return HttpResponse("Account Not Found")


@login_required()
def sellerindex(request):
    sellers = Seller.objects.all()
    seller_usernames = [seller.user.username for seller in sellers]
    p = [seller.company_name for seller in sellers]
    print(seller_usernames)
    crecord = None
    allde = []
    Order = Orders.objects.all()

    desc = []
    names = []
    for i in seller_usernames:
        if i == request.user.username:
            sellername = i
            Order1 = Orders.objects.all().values('items_json', 'name')
            for i in Order1:
                s = ""
                t = " "
                name = ""
                qty = ""
                sum = 0
                for value in i:
                    a = i.get(value)
                    flag = 0
                    for key in a:
                        if flag == 1:
                            qty = key
                            flag = 0
                        if sum == 0 and key == "[":
                            flag = 1
                        if key == ',':
                            sum = sum + 1
                        if sum == 1 and key != '"' and key != ',' and key != "(":
                            t = t + key

                        if sum == 2 and key != "'" and key != "," and key != " " and key != '"':
                            s = s + key

                        if sum == 3 and key != "," and key != "}" and key != "]" and key != "0" and key != "1" and key != "2" and key != "3" and key != "4" and key != "5" and key != "6" and key != "7" and key != "8" and key != "9":
                            name = name + key
                if s == sellername:
                    desc.append(t)
                    names.append(name)
            print(names)
            print(desc)
            all = {}
            for i , j in itertools.product(names, desc):
                all.update({i: j})
            print(all)
            prod = Product.objects.all()
            allde.append([Order, prod, crecord, desc, sellername, all])
            params = {'allde' : allde}
            return render(request, 'shopp/sellerindex.html', params)
    return HttpResponse("No Account Found")


@login_required()
def thanks(request):
    if request.method == 'POST':
        status = request.POST.get('status', '')
        print(status)
        print(request.POST)
        send_mail("Message  ", status, "akshkhnay@gmail.com", ["akshaykhn7@gmail.com"], fail_silently=False)
        return HttpResponse("Thank You for sending. Your pay will be sent to you by admin to your account")

#Tracking Page

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shopp/tracker.html')

#About Page


def about(request):
    return render(request, 'shopp/about.html')

#Contact Page


def contact(request):
    return render(request, 'shopp/contact.html')

#Product View


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'shopp/prodView.html', {'product': product[0]})


# Checkout
def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        a = json.loads(items_json)
        a1=0
        a2=""
        for key,value in a.items():
            a1=value[0]
            a2= value[1]
        a21 = Product.objects.get(product_name=a2)
        id= a21.id
        prod = Product.objects.get(id=id)

        names = [prod.product_name for prod in Product.objects.all()]
        for i in names:
            if i == a2:
                prod.quantity = prod.quantity - a1
                if prod.quantity == 0:
                    prod.save()
                    messages.info(request, 'Order has gone out of stock')
                    return render(request, 'shopp/checkout.html')



        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shopp/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shopp/checkout.html')

# Tracking


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request, 'shopp/tracker.html')

#Search


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shopp/search.html', params)
