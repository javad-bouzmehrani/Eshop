from django.db import models
from django.db.models.signals import pre_save

from eshop_products.models import product
from .utils import unique_slug_generator
# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=100 , verbose_name='نام برچسب')
    slug = models.SlugField(blank=True, allow_unicode=True, default='' ,verbose_name='اسلاگ')
    active = models.BooleanField(default=True ,verbose_name='وضعیت فعال بودن')
    timestamp = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(product , blank=True)

    def __str__(self):
        return self.title

def pre_save_tag(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_tag, sender=Tag)