from django.db import models

# Create your models here.
class Product_category(models.Model):
    title = models.CharField(max_length = 50 , verbose_name='تایتل')
    name = models.CharField(max_length = 50, verbose_name='نام')

    def __str__(self):
        return self.title
