import os
import random
from django.db import models

from product_category.models import Product_category


def get_file_extension(file):
    base_name = os.path.basename(file)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image(instance, filename):
    rand_name = random.randint(0, 999999)
    name, ext = get_file_extension(filename)
    final_name = f'{instance.id}-{instance.title}-{rand_name}{ext}'
    return f'products_images/{final_name}'

def upload_image_gallery(instance, filename):
    rand_name = random.randint(0, 999999)
    name, ext = get_file_extension(filename)
    final_name = f'{instance.id}-{instance.title}-{rand_name}{ext}'
    return f'product_gallery/{final_name}'

# Create your models here.
class product(models.Model):
    title = models.CharField(max_length=70,verbose_name='نام')
    description = models.TextField(verbose_name='توضیحات')
    price = models.DecimalField(max_digits=15, decimal_places=0,verbose_name='قیمت')
    old_price = models.DecimalField(
        max_digits=15, decimal_places=0,
        null=True, blank=True,
        verbose_name='قیمت قبل از تخفیف'
    )
    discount = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name='درصد تخفیف'
    )
    image = models.ImageField(upload_to=upload_image, null=True, blank=True,verbose_name='عکس')
    active = models.BooleanField(default=True,verbose_name='وضعیت فعال بود')
    time = models.DateTimeField(auto_now_add=True,verbose_name='زمان')
    cetegories = models.ManyToManyField(Product_category)
    featured = models.BooleanField(default=False , verbose_name='محصول ویژه')
    visits = models.IntegerField(default=0 , verbose_name='دیده شده')
    offer = models.BooleanField(default=False , verbose_name='محصول در تخفیف است؟')
    def __str__(self):
        return self.title
    def product_detail_url(self):
        return f"/product_detail/{self.id}/{self.title.replace(" ","-")}"

class Product_gallery(models.Model):
    title = models.CharField(max_length=70,verbose_name='نام')
    image = models.ImageField(upload_to=upload_image_gallery, null=True, blank=True, verbose_name='عکس')
    product = models.ForeignKey(product, on_delete=models.CASCADE , verbose_name='محصول')

    def __str__(self):
        return self.title
