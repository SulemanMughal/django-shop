from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # print(product)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        # print("Form is valued")
        cd = form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'], update_quantity=cd['update'])

    # print("Successfully added to cart")
    return redirect('cart:cart_detail')
    # return redirect('shop:product_list')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    # print("request is cate")
    cart = Cart(request)
    # print(cart)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
        initial={'quantity': item['quantity'],
        'update': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html', {'cart': cart,'coupon_apply_form': coupon_apply_form})