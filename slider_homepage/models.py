from django.db import models

from eshop_products.models import upload_image


# Create your models here.

class Slider(models.Model):
    title = models.CharField(max_length=100 , verbose_name='نام')
    description = models.TextField()
    link = models.URLField(verbose_name='لینک')
    image = models.ImageField(upload_to=upload_image)

    def __str__(self):
        return self.title