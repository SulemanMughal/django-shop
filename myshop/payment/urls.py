from django.conf.urls import url
from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _


app_name = 'payment'
urlpatterns = [
    url(_(r'^process/$'), views.payment_process, name='process'),
    url(_(r'^done/$'), views.payment_done, name='done'),
    url(_(r'^canceled/$'), views.payment_canceled, name='canceled'),
    path('api/checkout-session/', views.create_checkout_session, name='api_checkout_session'),
    path('success/<int:order_id>', views.payment_success, name='success'),
    path('failed/<int:order_id>', views.payment_fail, name='failed'),
]