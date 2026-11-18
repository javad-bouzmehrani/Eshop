from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from eshop_order.forms import User_neworder_Form
from eshop_order.models import Order, OrderItem
from eshop_products.models import product
from django.core.exceptions import PermissionDenied

def order_page(request):
    return render(request, 'order/order.html', {})


def add_new_order(request):
    if request.method != "POST":
        return redirect("/product_detail/")

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if not request.user.is_authenticated:
        if is_ajax:
            return JsonResponse(
                {
                    "ok": False,
                    "login_required": True,
                    "redirect": "/auth",
                    "message": "برای افزودن به سبد ابتدا وارد شوید",
                },
                status=401,
            )
        return redirect("/auth")

    form = User_neworder_Form(request.POST)

    if not form.is_valid():
        if is_ajax:
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)
        return redirect("/product_detail/")

    order = (
        Order.objects
        .filter(user=request.user, paid=False)
        .order_by("-id")
        .first()
    )
    if order is None:
        order = Order.objects.create(user=request.user, paid=False)

    product_id = form.cleaned_data.get("product_id")
    count = form.cleaned_data.get("count") or 1
    if count < 1:
        count = 1

    product_p = get_object_or_404(product, id=product_id)

    OrderItem.objects.create(
        order=order,
        product=product_p,
        count=count,
        price=product_p.price,
    )

    if is_ajax:
        return JsonResponse({
            "ok": True,
            "message": "به سبد خرید اضافه شد",
            "cart_count": order.orderitem_set.count(),
        })

    return redirect(
        f'/product_detail/{product_p.id}/{product_p.title.replace(" ", "-")}'
    )

@login_required(login_url="/auth")
def cart_detail(request):
    order = (
        Order.objects
        .filter(user=request.user, paid=False)
        .order_by('-id')
        .first()
    )
    details = order.orderitem_set.all() if order else []

    if order:
        subtotal = order.subtotal()
        discount = order.discount()
        total    = order.total()
        points   = int(total // 1000)
    else:
        subtotal = 0
        discount = 0
        total    = 0
        points   = 0

    context = {
        'order': order,
        'details': details,
        'subtotal': subtotal,   # جمع قیمت قبل از تخفیف
        'discount': discount,   # مجموع تخفیف‌ها
        'total': total,         # مبلغ قابل پرداخت
        'points': points,
    }
    return render(request, 'order/order.html', context)




@login_required(login_url="/auth")
def remove_card_item(request, *args, **kwargs):
    order_item = get_object_or_404(OrderItem, id=kwargs['order_id'])

    if order_item.order.user_id != request.user.id:
        raise PermissionDenied

    order_item.delete()
    return redirect('/order')






