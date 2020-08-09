from django.db import models
import random
import os
from django.utils.text import slugify
from django.urls import reverse


def get_file_name(filepath):
    base_name=os.path.basename(filepath)
    name,ext=os.path.splitext(base_name)
    return name,ext


def upload_image_path(instance,filename):
    new_filename=random.randint(1,10000000000000000000)
    name,ext=get_filename_ext(filename)
    final_filename=str(new_filename)+str(ext)
    return "products/"+str(new_filename)+"/"+str(final_filename)
class ProductManager(models.Manager):
    def get_by_id(self,id):
        qs= self.get_queryset().filter(id=id)
        if qs.count()==1:
            return qs.first()
        return None
        
    def featured(self):
        return self.get_queryset().filter(featured=True)

    def all(self):
        return self.get_queryset().active()

    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)

class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)
    def active(self):
        return self.filter(active=True)
    def search(self,query):
        lookups=(Q(title__icontains=query)|Q(desc__icontains=query)|Q(price__icontains=query)|Q(tag__title__icontains=query))
        return self.filter(lookups).distinct()
        
                # Create your models here.
class Product(models.Model):
    title=models.CharField( max_length=150)
    slug=models.SlugField(blank=True,unique=True)
    desc=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField( upload_to="products",blank=True,null=True)
    featured=models.BooleanField(default=False)
    active=models.BooleanField(default=False)
    created=models.DateTimeField( blank=True, auto_now_add=True)

    objects=ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:product-detail", kwargs={"slug": self.slug})
    
    def descr(self):
        return self.desc[:100]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)    
