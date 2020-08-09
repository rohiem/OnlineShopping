from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.views.generic import ListView,DetailView
from .models import Product
from cart.models import Cart
# Create your views here.


class ProductList(ListView):
#    queryset=Product.objects.all()
    template_name="products/product_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Product.objects.all()
        return context
    def get_queryset(self,*args, **kwargs):
        request=self.request
        return Product.objects.all()
    

class ProductDetail(DetailView):
    queryset=Product.objects.all()
    template_name="products/product_detail.html"

    def get_context_data(self,*args ,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        request= self.request
        cart_obj,new_obj=Cart.objects.new_or_get(request)
        context['cart']=cart_obj
        return context


    def get_object(self,*args,**kwargs ):
        request=self.request
        slug=self.kwargs['slug']
        instance=get_object_or_404(Product,slug=slug,active=True)
        if instance is None:
            raise Http404("product doesn't exist")
        return instance


    def get_queryset(self,*args, **kwargs):
        request=self.request
        slug=self.kwargs['slug']
        return Product.objects.filter(slug=slug)



class ProductFList(ListView):
#    queryset=Product.objects.all()
    template_name="products/product_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Product.objects.featured()
        return context
    def get_queryset(self,*args, **kwargs):
        request=self.request
        return Product.objects.featured()
    
'''
class ProductFDetail(DetailView):
    queryset=Product.objects.featured()
    template_name="products/product_detail.html"
'''