from .cart import Cart
from django.conf import settings

def cart(request):
    return {'cart': Cart(request)}


def get_stripe_key(request):
    return {'get_stripe_key': settings.STRIPE_PUBLISHABLE_KEY}