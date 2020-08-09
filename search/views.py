from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView
# Create your views here.
from django.db.models import Q



class SearchProductList(ListView):
#    queryset=Product.objects.all()
    template_name="products/product_list.html"

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context["object_list"] = Product.objects.all()
#        return context
    def get_queryset(self,*args, **kwargs):
        request=self.request
        query =request.GET.get('search',None)
        if query is not None:
            return Product.objects.filter(Q(title__icontains=query)|Q(tag__title__icontains=query))
        return Product.objects.featured()
    
