"""OnlineShopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import home_page,about_page,contact_page,login_page,register_page,guest_login_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from addresses.views import checkout_address_create_view,checkout_address_reuse_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_page,name="home"),
    path('about',about_page,name="about"),
    path('contact',contact_page,name="contact"),
    path('login',login_page,name="login"),
    path('signup',register_page,name="signup"),
    path('signup/guest',guest_login_view,name="guest_signup"),
    path('checkout/address/create',checkout_address_create_view,name="checkout_address_create"),
    path('checkout/address/reuse',checkout_address_reuse_view,name="checkout_address_reuse"),

    path('logout',LogoutView.as_view(template_name="logout.html"),name="logout"),
    path("products" ,include("products.urls")),
    path("search/" ,include("search.urls")),
    path("cart/" ,include("cart.urls")),

]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)