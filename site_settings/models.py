import os
import random
from django.db import models


def get_file_extension(file):
    base_name = os.path.basename(file)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image(instance,filename):
    rand_name = random.randint(0, 999999)
    name, ext = get_file_extension(filename)
    final_name = f'{rand_name}{ext}'
    return f'settings/{final_name}'

# Create your models here.
class Setting(models.Model):
    site_name = models.TextField(max_length=40)
    phone_support = models.CharField(max_length=20)
    tag_up_left = models.CharField(max_length=50)
    tag_up_right = models.CharField(max_length=50)
    copyright_text = models.TextField(max_length=125 , verbose_name="copy right text")
    description_down_right = models.TextField(max_length=150,verbose_name='about us')
    logo = models.ImageField(upload_to=upload_image , null=True, blank=True)

    def __str__(self):
        return 'Site settings'
