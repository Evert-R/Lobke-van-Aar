import uuid

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from works.models import work_items

# Create your models here.


class orders(models.Model):
    order_number = models.CharField(max_length=32, null=False) 
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)    
    paid = models.BooleanField(default=False)
    pay_method = models.CharField(blank=True, max_length=10)    
    sent = models.BooleanField(default=False)
    sent_date = models.DateTimeField(blank=True, null=True)
    sent_method = models.CharField(blank=True, max_length=10)
    sent_tracking = models.CharField(blank=True, max_length=254)
    total = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    address1 = models.CharField(blank=True, max_length=50)
    address2 = models.CharField(blank=True, max_length=50)
    postcode = models.CharField(blank=True, max_length=50)
    city = models.CharField(blank=True, max_length=50)
    country = models.CharField(blank=True, max_length=50)
    telephone = models.CharField(blank=True, max_length=25)
    shipping = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.order_number       


class order_items(models.Model):
    order = models.ForeignKey(orders, null=False, on_delete=models.CASCADE, related_name='orderitems')
    work_item = models.ForeignKey(
        work_items, null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)
    price = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)


    def __str__(self):
        return "{0} {1} @ {2}".format(
            self.quantity, self.work_item.title, self.work_item.shop_settings.price)
