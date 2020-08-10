from django.urls import path
from .views import cart_home,cart_update,checkout_home,checkout_done_view,charge,successMsg

app_name="cart"
urlpatterns = [
    path('',cart_home,name="cart"),
    path('cart_update',cart_update,name="cart_update"),
    path('checkout',checkout_home,name="checkout"),
    path('checkout/success',checkout_done_view,name="success_checkout"),
    path('charge/', charge, name="charge"),
    path('success/<str:args>/',successMsg, name="success"),

    ]