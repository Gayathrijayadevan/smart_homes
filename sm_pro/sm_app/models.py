from django.db import models
from django.contrib.auth.models import User
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


