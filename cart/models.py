from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save,m2m_changed
import decimal
from decimal import *

# Create your models here.

User=settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self,request):
            
        cart_id=request.session.get("cart_id",None)
    
        qs=self.get_queryset().filter(id=cart_id)
        if qs.count()==1:
            new_obj=False

            cart_obj =qs.first()
            print("cart id exists")

            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user=request.user
                cart_obj.save()

        else:
                cart_obj=Cart.objects.new_cart(user=request.user)
                new_obj=True
                request.session['cart_id']=cart_obj.id

        return cart_obj,new_obj

    def new_cart(self,user=None):
        user_obj=None
        if user is not None:
            if user.is_authenticated:
                user_obj=user
        return self.model.objects.create(user=user_obj)





class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE ,null=True,blank=True)
    products=models.ManyToManyField(Product,blank=True)
    total=models.DecimalField(default=0.00,max_digits=8, decimal_places=2)
    sub_total=models.DecimalField(default=0.00,max_digits=8, decimal_places=2)
    updated=models.DateTimeField( auto_now=True)
    created=models.DateTimeField(auto_now_add=True)


    objects=CartManager()
    def __str__(self):
        return str(self.id)



def m2m_changed_cart_reciever(sender,instance,action,*args, **kwargs):
    print(action)
    if action == "post_add" or action == "post_remove" or action == "post_clear":
        products=instance.products.all()
        total=0
        for x in products:
            total+=x.price
        print(total)
        if instance.sub_total!=total:
            instance.sub_total=total
            instance.save()

m2m_changed.connect(m2m_changed_cart_reciever,sender=Cart.products.through)   


def pre_save_cart_receiver(sender,instance,*args, **kwargs):
    if instance.sub_total>0:
        instance.total= decimal.Decimal(float(instance.sub_total))*decimal.Decimal(float(.5))
    else:
        instance.total=0.00

pre_save.connect(pre_save_cart_receiver,sender=Cart)