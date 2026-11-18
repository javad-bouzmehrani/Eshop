from django.core.exceptions import ValidationError
from django.db import models

from eshop_products.models import upload_image


class Slider(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    image = models.ImageField(upload_to=upload_image)

    def __str__(self):
        return self.title


class Promo(models.Model):
    MAX_COUNT = 2

    title = models.CharField(max_length=80,verbose_name='نام')
    description = models.CharField(max_length=120, blank=True, verbose_name='توضیحات')
    tag = models.CharField(max_length=40,verbose_name='تگ')
    image = models.ImageField(upload_to=upload_image)

    def __str__(self):
        return self.title

    def clean(self):
        if not self.pk and Promo.objects.count() >= self.MAX_COUNT:
            raise ValidationError(
                f"فقط {self.MAX_COUNT} پرومو مجاز است. برای تغییر، ابتدا یکی را ویرایش کنید."
            )

    def save(self, *args, **kwargs):
        if not self.pk and Promo.objects.count() >= self.MAX_COUNT:
            raise ValidationError(
                f"فقط {self.MAX_COUNT} پرومو مجاز است."
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if Promo.objects.count() <= self.MAX_COUNT:
            raise ValidationError(
                "حداقل باید دو پرومو وجود داشته باشد؛ حذف مجاز نیست."
            )
        super().delete(*args, **kwargs)