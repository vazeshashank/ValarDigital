from django.contrib.auth.models import AbstractUser
from django.db import models

class UserLog(AbstractUser):  #Vendor-1,Customer-2
    user_type = models.IntegerField(null=True)

class Category(models.Model):
    category = models.CharField(max_length=100)  

    def __str__(self):
        return self.category 

class Products(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='static/images/')
    username = models.CharField(max_length=200,null=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return (self.brand)+" "+(self.item_name)
        




