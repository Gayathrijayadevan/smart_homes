from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus

# Create your models here.

class Category(models.Model):
    Category_name=models.TextField()
    def __str__(self):
        return self.Category_name

class Product(models.Model):
    pid=models.TextField()
    name=models.TextField()
    des=models.TextField()
    price=models.IntegerField()
    offer_price=models.IntegerField()
    stock=models.IntegerField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand=models.TextField(null=True, blank=True)
    dimension=models.TextField(null=True, blank=True)
    weight=models.TextField(null=True, blank=True)
    img=models.FileField()
    def __str__(self):
        return self.name


class Cart(models.Model) :
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()

class User_details(models.Model)  :
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.TextField()
    phone=models.IntegerField()
    pincode=models.IntegerField()
    state=models.TextField()
    country=models.TextField()   

class Buy(models.Model) :
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User_details,on_delete=models.CASCADE)
    qty=models.IntegerField()
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True)
    payment_method=models.TextField(null=True, blank=True )


class Enquire(models.Model):
    name=models.TextField()
    email=models.EmailField()
    product=models.TextField()
    brand=models.TextField()
    enq=models.TextField()
    Phone=models.IntegerField()

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.IntegerField(default=5)  # 1 to 5 rating
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.name}"

class Schedule(models.Model):
    name=models.TextField()
    email=models.EmailField()
    Phone=models.IntegerField()
    date=models.DateField(null=True, blank=True)
    time=models.TimeField(null=True, blank=True)

class Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"




