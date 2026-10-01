from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2,max_digits=20)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/',null=True,blank=True)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.product.name

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    address=models.TextField()
    total=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=100,
                            choices=[('Pending','Pending'),
                                     ('Accepted','Accepted'),
                                     ('Rejected','Rejected'),
                                     ('Cancelled','Cancelled'),
                                     ('Processing','Processing'),
                                     ('Delivered','Delivered')
                                     ],default='Pending')


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(decimal_places=2,max_digits=20)