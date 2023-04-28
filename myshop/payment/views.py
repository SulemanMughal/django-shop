import json
from decimal import Decimal
from django.conf import settings
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
# from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.db.models import Sum
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from orders.models import OrderItem
from cart.cart import Cart
from orders.forms import OrderCreateForm

def payment_success(request, order_id):
    cart = Cart(request)
    # print(request.POST)
    # print(request.GET)
    # print(request.session[""])
    cart.clear()
    checkout_session = stripe.checkout.Session.retrieve(
        request.GET['session_id'],
    )
    order = Order.objects.get(pk = order_id)
    order.paid = True
    order.stripe_payment_intent = checkout_session.payment_intent
    order.save()
    
    # print()

    template_name = "payment/payment_success.html"
    context = {
        "order_id" : order.id
    }
    return render(request, template_name, context)

def payment_fail(request, order_id):
    # cart = Cart(request)
    order = Order.objects.get(pk = order_id)
    order.delete()
    template_name = "payment/payment_failed.html"
    context = {
    }
    return render(request, template_name, context)

# class PaymentSuccessView(TemplateView):
#     # pass
    

    

# class PaymentFailedView(TemplateView):
#     # pass
#     template_name = "payment/payment_failed.html"


@csrf_exempt
def create_checkout_session(request ):

    request_data = json.loads(request.body)
    # print(request_data)s
    cart = Cart(request)
    # order = get_object_or_404(Order, pk=id)
    temp = []
    for item in cart:
        temp.append({
            "price" : item['product'].stripe_price_id,
            "quantity" : item["quantity"]
        })

    
    # for item in cart:
        # temp.append({

        # })
        # OrderItem.objects.create(order=order,
        # product=item['product'],
        # price=item['price'],
        # quantity=item['quantity'])

    try:
        # form = OrderCreateForm(request.POST)
        # if form.is_valid():
        #     order = form.save()
        #     request.session[order_id] = 
        # print(request_data)
        form = OrderCreateForm(request_data)
        order = None
        if form.is_valid():
            # order = form.save()
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'])
        else:
            return JsonResponse({'sessionId': "error"})
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            # Customer Email is optional,
            # It is not safe to accept email directly from the client side
            customer_email = request_data['email'],
            payment_method_types=['card'],
            line_items=temp,
            mode='payment',
            discounts=[{
                'coupon': cart.coupon.stripe_coupon_id,
            }],
            success_url=request.build_absolute_uri(
                reverse('payment:success', kwargs={"order_id" : order.id })
            )  + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('payment:failed',  kwargs={"order_id" : order.id})),
        )
        # print(checkout_session.id)
        return JsonResponse({'sessionId': checkout_session.id})
    except Exception as e:
        print(e)
        return JsonResponse({'sessionId': "error"})


    # OrderDetail.objects.create(
    #     customer_email=email,
    #     product=product, ......
    # )

    # order = OrderDetail()
    # order.customer_email = request_data['email']
    # order.product = product
    # order.stripe_payment_intent = checkout_session['payment_intent']
    # order.amount = int(product.price * 100)
    # order.save()

    # return JsonResponse({'data': checkout_session})
    





def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()
    paypal_dict = {
    'business': settings.PAYPAL_RECEIVER_EMAIL,
    'amount': '%.2f' % order.get_total_cost().quantize(
    Decimal('.01')),
    'item_name': 'Order {}'.format(order.id),
    'invoice': str(order.id),
    'currency_code': 'USD',
    'notify_url': 'http://{}{}'.format(host,
    reverse('paypal-ipn')),
    'return_url': 'http://{}{}'.format(host,
    reverse('payment:done')),
    'cancel_return': 'http://{}{}'.format(host,
    reverse('payment:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request,
    'payment/process.html',
    {'order': order, 'form':form})


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')