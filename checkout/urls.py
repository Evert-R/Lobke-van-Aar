from django.urls import path

from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.check_out, name='check_out'),
    path("create-payment-intent", views.create_payment, name="create_payment_intent"),
    path("cache-checkout-data", views.cache_checkout_data, name="cache_checkout_data"),
    path("payment-complete", views.payment_complete, name="payment_complete"),
    ]
