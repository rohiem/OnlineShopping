from django.db import models
from products.models import Product
from django.utils.text import slugify

# Create your models here.
class Tag(models.Model):
    title=models.CharField(max_length=50)
    slug=models.SlugField(blank=True)
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    products=models.ManyToManyField(Product,blank=True)

    
    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)   