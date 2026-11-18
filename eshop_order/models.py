from django.contrib.auth.models import User
from django.db import models
from eshop_products.models import product

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='کاربر')
    paid = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')
    pay_date = models.DateTimeField(blank=True, null=True,verbose_name='زمان پرداخت')

    def __str__(self):
        return self.user.get_full_name()

    # جمع قیمت قبل از تخفیف (old_price × count)
    def subtotal(self):
        total = 0
        for item in self.orderitem_set.all():
            total = total + item.old_price()
        return total

    # جمع تخفیف‌ها ((old_price − price) × count)
    def discount(self):
        total = 0
        for item in self.orderitem_set.all():
            total = total + item.old_price() - item.total_price()
        return total

    # مبلغ قابل پرداخت (price × count)
    def total(self):
        total = 0
        for item in self.orderitem_set.all():
            total = total + item.total_price()
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='سبد')
    product = models.ForeignKey(product,on_delete=models.CASCADE,verbose_name='محصول')
    count = models.IntegerField(verbose_name='تعداد')
    price = models.IntegerField(verbose_name='قیمت')
    def __str__(self):
        return self.product.title

    def old_price(self):
        if self.product.old_price:
            return self.product.old_price * self.count
        return 0

    def total_price(self):
        return self.price * self.count