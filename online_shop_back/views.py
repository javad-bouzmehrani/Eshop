from django.contrib.auth import authenticate, login as auth_login , get_user_model , logout
from django.shortcuts import render, redirect
from django.contrib import messages
from online_shop_back.forms import Login , Register
from slider_homepage.models import Slider
from sidepromo.models import Promo
from site_settings.models import Setting
from eshop_order.models import Order
from eshop_products.models import product, Product_gallery


def header(request):
    setting = Setting.objects.first()

    cart_count = 0
    if request.user.is_authenticated:
        order = (
            Order.objects
            .filter(user=request.user, paid=False)
            .order_by('-id')
            .first()
        )
        if order:
            cart_count = order.orderitem_set.count()

    context = {
        'setting': setting,
        'cart_count': cart_count,
    }
    return render(request, 'base/header.html', context)


def footer(request):
    setting = Setting.objects.first()
    context = {
        'setting': setting,
    }
    return render(request, 'base/footer.html', context)


def home_page(request):
    featured_products = product.objects.filter(featured=True)
    setting = Setting.objects.first()
    sliders = Slider.objects.all()
    promos = Promo.objects.all()
    most_visits = product.objects.order_by('-visits').all()[:4]
    offer_products = product.objects.filter(offer=True)
    context = {
        'sliders': sliders,
        'promos': promos,
        'setting':setting,
        'featured_products':featured_products,
        'most_visits':most_visits,
        'offer_products':offer_products
    }
    return render(request, 'index.html', context)


def shop_cart(request):
    return render(request, 'shopping_cart/shop_cart.html', {})




User_get = get_user_model()


def login_view(request):
    active_tab = request.session.get('active_auth_tab', 'login')

    login_form = Login()
    register_form = Register()

    context = {
        'title': 'Login page',
        'login_form': login_form,
        'register_form': register_form,
        'message': '',
        'active_tab': active_tab,
    }

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            request.session['active_auth_tab'] = 'login'
            context['active_tab'] = 'login'
            login_form = Login(request.POST)
            context['login_form'] = login_form

            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, 'ورود موفق')
                    return redirect('/')
                else:
                    context['message'] = 'نام کاربری یا رمز عبور اشتباه است'

        elif 'register_submit' in request.POST:
            request.session['active_auth_tab'] = 'register'
            context['active_tab'] = 'register'
            register_form = Register(request.POST)
            context['register_form'] = register_form

            if register_form.is_valid():
                full_name = register_form.cleaned_data.get('full_name')
                phone = register_form.cleaned_data.get('phone')
                password = register_form.cleaned_data.get('password')

                new_user = User_get.objects.create_user(
                    username=phone,
                    password=password,
                    first_name=full_name,
                )
                auth_login(request, new_user)
                return redirect('/')

    return render(request, 'auth/login_reg.html', context)

def log_out(request):
    logout(request)
    return redirect('/auth')

