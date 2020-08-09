from django.shortcuts import render,redirect
from .models import Cart
from products.models import Product
from addresses.forms import AddressForm
from orders.models import Order
from OnlineShopping.forms import LoginForm,GuestForm
from billing.models import BillingProfile,GuestEmail
from addresses.models import Address

""" def cart_create(user=None):
    cart_obj=Cart.objects.create(user=none)
    print("new cart created")
    return cart_obj """

def cart_home(request):
    cart_obj,new_obj=Cart.objects.new_or_get(request)
    products=cart_obj.products.all()


#     total=0
#     for x in products:
#         total+=x.price
#     print(total)
#     cart_obj.total=total
#     cart_obj.save()


    context={"cart":cart_obj}
    return render(request,"cart_home.html",context)  
""" cart_id=request.session.get("cart_id",None)
   
    qs=Cart.objects.filter(id=cart_id)
    if qs.count()==1:
        cart_obj =qs.first()
        print("cart id exists")

        if request.user.is_authenticated and cart_obj.user is None:
            cart_obj.user=request.user
            cart_obj.save()

    else:
            cart_obj=Cart.objects.new_cart(user=request.user)
            request.session['cart_id']=cart_obj.id 
"""

#        print(cart_id)
#        cart_obj=Cart.objects.get(id=cart_id)
#    print(request.session.session_key)
#    print(dir(request.session))
#    print(request.session.set_expiry(300))
#    request.session['user']=request.user.username


def cart_update(request):
    product_id=request.POST.get("product_id")
    if product_id is not None:
        try:
            obj =Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("cart:cart")
        
        cart_obj,new_obj=Cart.objects.new_or_get(request)
        if obj in cart_obj.products.all():
            cart_obj.products.remove(obj)

        else:
            cart_obj.products.add(obj)
        request.session["cart_items"]=cart_obj.products.count()

    return redirect("cart:cart")



def checkout_home(request):
    cart_obj,cart_created=Cart.objects.new_or_get(request)
    order_obj=None
    if cart_created or cart_obj.products.count()==0:
        return redirect("cart:cart")


    login_form =LoginForm()
    guest_form=GuestForm()
    address_form=AddressForm()
    billing_address_form=AddressForm()
    billing_address_id =request.session.get("billing_address_id",None)
    shipping_address_id =request.session.get("shipping_address_id",None)

    billing_profile,billing_profile_created=BillingProfile.objects.new_or_get(request)

    address_qs=None
    if billing_profile is not None:
        address_qs=Address.objects.filter(billing_profile=billing_profile)
        shipping_address_qs=address_qs.filter(address_type="shipping")
        billing_address_qs=address_qs.filter(address_type="billing")
        order_obj,order_obj_created=Order.objects.new_or_get(billing_profile,cart_obj)
        if shipping_address_id :
            order_obj.shipping_address=Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id :
            order_obj.billing_address= Address.objects.get(id=billing_address_id)    
            del request.session["billing_address_id"]
        if shipping_address_id or billing_address_id:
            order_obj.save()
    if request.method=="POST":
        is_done =order_obj.check_done()
        if is_done:  
            order_obj.mark_paid()
            request.session["cart_items"]=0
            del request.session["cart_id"]

            return redirect("cart:success")


    context={"object":order_obj,
    "billing_profile":billing_profile,
    "login_form":login_form,
    "guest_form":guest_form,
    "address_form":address_form,
    "billing_address_form":billing_address_form,
    "address_qs":address_qs,

    }
    return render(request,"checkout.html",context)



def checkout_done_view(request):
    return render(request, "checkout-done.html", {})