from django.urls import path
from .views import ProductList,ProductDetail
# ,ProductFList
#ProductFDetail ,

app_name="products"
urlpatterns = [
    path('',ProductList.as_view(),name="products"),
    path('<slug:slug>',ProductDetail.as_view(),name="product-detail"),
#    path('f',ProductFList.as_view(),name="fproducts"),
#    path('f/<slug:slug>',ProductFDetail.as_view(),name="product-fdetail"),
    ]