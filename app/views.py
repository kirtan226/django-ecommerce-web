from django.db.models import Q, QuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced, CoverImage
from .forms import CustomerRegistrationForm, CustomerProfileForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.conf import settings
import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))


# username - kitan_patel
# email - kirtan@gmail.com
# pass- kitan_patel22 --> 123456@hello

# new22
# old -  newuser123456
# new - hello123hello

# admin - hello@123newad
# 123@helloadnew
# resetpass = new22621
# resetpass = 123456@hello

# kirtan22 - kirtan22@gmail.com - kirtan@22

# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        cover_images = CoverImage.objects.filter(is_active=True)

        parameter = {
            'topwears': topwears,
            'bottomwears': bottomwears,
            'mobiles': mobiles,
            'laptops': laptop,
            'cover_images': cover_images,
        }

        return render(request, 'app/home.html', parameter)


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

@method_decorator(login_required, name='dispatch')
class Productdetails(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        description_list = product.description.split(' .')
        saved_price = product.selling_price - product.discounted_price
        # print("============",saved_price)

        cart = Cart.objects.filter(user=request.user).values_list('product_id', flat=True)

        parameter = {'product': product, 'description_list': description_list, 'saved_price': saved_price, 'cart': cart}
        return render(request, 'app/productdetail.html', parameter)


def searchMatch(query, item):
    query = query.lower()
    if (query in item.title.lower() or
        query in item.description.lower() or
        query in item.category.lower() or
        query in item.brand.lower()):
        return True
    return False

def search(request):
    query = request.GET.get('search').strip()
    allproducts = []

    if query:
        # Filter products directly using the search query
        allproducts = Product.objects.filter(
            Q(title__icontains=query) |
            # Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(brand__icontains=query)
        )

    # print(f"Search Query: '{query}'")
    # print(f"Number of Products Found: {allproducts.count()}")

    parameter = {'allproducts': allproducts, 'query': query}
    return render(request, 'app/search.html', parameter)


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    cart_item = Cart.objects.filter(user=user, product=product).first()
    created = cart_item is None
    if created:
        Cart.objects.create(user=user, product=product)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'added': created,
            'message': 'Product added to cart' if created else 'Product already in cart',
            'cart_item_count': Cart.objects.filter(user=user).count(),
        })

    return redirect('showcart')



def show_cart(request):
    if request.user.is_authenticated:

        user = request.user
        cart = Cart.objects.filter(user=user)

        l = len(cart)
        shipping_charges = 70.0

        cart_product = Cart.objects.filter(user=user).select_related('product')
        total = 0
        if cart_product:
            for p in cart_product:
                temp = (p.quantity * p.product.discounted_price)
                total += int(temp)

        if total <= 1500:
            total_amount = total + shipping_charges
            ship = True
        else:
            total_amount = total
            ship = False

        params = {'carts': cart, 'total': total, 'cart_product': cart_product, 'total_amount': total_amount, 'len': l,
                  'ship': ship}
        return render(request, 'app/addtocart.html', params)


def get_cart_summary(user):
    total = 0
    for item in Cart.objects.filter(user=user).select_related('product'):
        total += int(item.quantity * item.product.discounted_price)

    shipping_charges = 70.0
    ship = total <= 1500 and total > 0
    total_amount = total + shipping_charges if ship else total

    return {
        'amount': total,
        'totalamount': total_amount,
        'ship': ship,
        'cart_item_count': Cart.objects.filter(user=user).count(),
        'cart_empty': not Cart.objects.filter(user=user).exists(),
    }


@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        if c is None:
            return JsonResponse({'error': 'Cart item not found'}, status=404)

        c.quantity += 1
        c.save()
        data = {'quantity': c.quantity, 'removed': False}
        data.update(get_cart_summary(request.user))
        return JsonResponse(data)


@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        if c is None:
            return JsonResponse({'error': 'Cart item not found'}, status=404)

        removed = False
        if c.quantity <= 1:
            c.delete()
            removed = True
            quantity = 0
        else:
            c.quantity -= 1
            c.save()
            quantity = c.quantity

        data = {'quantity': quantity, 'removed': removed}
        data.update(get_cart_summary(request.user))
        return JsonResponse(data)


@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).delete()
        data = {'quantity': 0, 'removed': True}
        data.update(get_cart_summary(request.user))
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


def profile(request):
    return render(request, 'app/profile.html')


@login_required()
def address(request):
    add = Customer.objects.filter(user=request.user)
    parameter = {'address': add, 'active': 'btn-primary'}
    return render(request, 'app/address.html', parameter)


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    if len(op) >= 1:

        parameter = {'orderplaced': op}
        return render(request, 'app/orders.html', parameter)
    else:
        return render(request, 'app/orders.html')


# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request, data=None):

    mobiles = Product.objects.filter(category='M')

    price_ranges = {
        'below_15k': (0, 15999),
        '16k-35k': (16000, 35999),
        '36k-50k': (36000, 50999),
        '51k-75k': (51000, 75999),
        '76k-90k': (76000, 90999),
        '91k-1l': (91000, 100999),
        'more_than_1l': (110000, float('inf'))
    }

    # Get price filter from request
    price_filter = request.GET.get('price', 'all')

    # Filter laptops based on the selected price range
    if price_filter in price_ranges:
        min_price, max_price = price_ranges[price_filter]
        mobiles = Product.objects.filter(category='M', discounted_price__gte=min_price, discounted_price__lte=max_price)
    else:
        mobiles = Product.objects.filter(category='M')

    parameter = {'mobiles': mobiles}
    return render(request, 'app/mobile.html', parameter)


def topwear(request):
    top = Product.objects.filter(category='TW')

    price_ranges = {
        'below_15k': (0, 15999),
        '16k-35k': (16000, 35999),
        '36k-50k': (36000, 50999),
        '51k-75k': (51000, 75999),
        '76k-90k': (76000, 90999),
        '91k-1l': (91000, 100999),
        'more_than_1l': (110000, float('inf'))
    }

    # Get price filter from request
    price_filter = request.GET.get('price', 'all')

    # Filter laptops based on the selected price range
    if price_filter in price_ranges:
        min_price, max_price = price_ranges[price_filter]
        top = Product.objects.filter(category='TW', discounted_price__gte=min_price, discounted_price__lte=max_price)
    else:
        top = Product.objects.filter(category='TW')

    parameter = {'top': top}
    return render(request, 'app/topwear.html', parameter)


def bottomwear(request):
    # bottom = Product.objects.filter(category='BW')

    price_ranges = {
        'below_15k': (0, 15999),
        '16k-35k': (16000, 35999),
        '36k-50k': (36000, 50999),
        '51k-75k': (51000, 75999),
        '76k-90k': (76000, 90999),
        '91k-1l': (91000, 100999),
        'more_than_1l': (110000, float('inf'))
    }

    # Get price filter from request
    price_filter = request.GET.get('price', 'all')

    # Filter laptops based on the selected price range
    if price_filter in price_ranges:
        min_price, max_price = price_ranges[price_filter]
        bottom = Product.objects.filter(category='BW', discounted_price__gte=min_price, discounted_price__lte=max_price)
    else:
        bottom = Product.objects.filter(category='BW')

    parameter = {'bottom': bottom}
    return render(request, 'app/bottomwear.html', parameter)


def laptop(request):
    lap = Product.objects.filter(category='L')

    price_ranges = {
        'below_15k': (0, 15999),
        '16k-35k': (16000, 35999),
        '36k-50k': (36000, 50999),
        '51k-75k': (51000, 75999),
        '76k-90k': (76000, 90999),
        '91k-1l': (91000, 100999),
        'more_than_1l': (110000, float('inf'))
    }

    # Get price filter from request
    price_filter = request.GET.get('price', 'all')

    # Filter laptops based on the selected price range
    if price_filter in price_ranges:
        min_price, max_price = price_ranges[price_filter]
        lap = Product.objects.filter(category='L', discounted_price__gte=min_price, discounted_price__lte=max_price)
    else:
        lap = Product.objects.filter(category='L')
    parameter = {'laptops': lap}
    return render(request, 'app/laptop.html', parameter)


# def login(request):
#  return render(request, 'app/login.html')

class EmailLoginView(LoginView):
    template_name = 'app/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        if Customer.objects.filter(user=self.request.user).exists():
            return reverse_lazy('ptoductview')
        return reverse_lazy('profile')


# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class customerregistration(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'New User Registered Successfully .')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)

    shipping_charges = 70.0
    total_amount = 0.0
    all = Cart.objects.all()
    cart_product = [p for p in all if p.user == request.user]
    print(cart_product)
    total = 0

    if cart_product:
        for p in cart_product:
            temp = (p.quantity * p.product.discounted_price)
            total += temp

    # with shipping charges
    print(type(total))
    if total <= 1500:
        total_amount = total + shipping_charges
        ship = True
        print("i am if ==========", total_amount)
    else:
        total_amount = total
        ship = False
        print("i am else without shipping ==========", total_amount)

    if isinstance(total_amount, QuerySet):
        total_amount = list(total_amount.values())
    if isinstance(add, QuerySet):
        add = list(add.values())
    DATA = {
        "amount": total_amount * 100,
        "currency": "INR",
        # "receipt": "receipt#1",
        "notes": {"address": add},

    }
    payment_order = client.order.create(data=DATA)
    payment_order_id = payment_order['id']

    print(payment_order_id)

    parameter = {'address': add, 'total': total, 'cart_product': cart_product, 'total_amount': total_amount,
                 'api_key': settings.RAZORPAY_API_KEY, 'payment_order_id': payment_order_id}
    return render(request, 'app/checkout.html', parameter)


def payment_success(request):
    return HttpResponse("Payment Successful")


def payment_cancel(request):
    return HttpResponse("Payment Cancelled")


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)

    l = len(cart)
    all = Cart.objects.all()
    amount = 0.0
    shipping_charges = 70.0
    total_amount = 0.0

    cart_product = [p for p in all if p.user == user]
    print(cart_product)
    total = 0
    if cart_product:
        for p in cart_product:
            temp = (p.quantity * p.product.discounted_price)
            total += int(temp)
    # with shipping charges
    print(type(total))

    if total <= 1500:
        total_amount = total + shipping_charges
        ship = True
        print("i am if ==========", total_amount)
    else:
        total_amount = total
        ship = False
        print("i am else without shipping ==========", total_amount)

    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, price=total_amount).save()
        c.delete()
    return redirect('orders')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        parameter = {'form': form, 'active': 'btn-primary'}
        return render(request, 'app/profile.html', parameter)

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
            messages.success(request, 'Your Data Has Been Updated Successfully.')
        parameter = {'form': form, 'active': 'btn-primary'}
        return render(request, 'app/profile.html', parameter)
