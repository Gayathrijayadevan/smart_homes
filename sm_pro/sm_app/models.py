from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    pid=models.TextField()
    name=models.TextField()
    des=models.TextField()
    price=models.IntegerField()
    offer_price=models.IntegerField()
    categorie=models.TextField()
    stock=models.IntegerField()
    img=models.FileField()

class Cart(models.Model) :
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()

class Buy(models.Model) :
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True)
