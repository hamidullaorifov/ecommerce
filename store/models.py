import email
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('sport','Sport'),
        ('telephone','Telephone & Accessories'),
        ('computer','Computer & Office'),
        ('furniture','Furniture'),
        ('shoes','Shoes'),
        ('jewellery','Jewellery & Watches')
    )
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField()


    def __str__(self):
        return self.name
    

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True,blank=True)

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    @property
    def get_total_count(self):
        total = sum(item.quantity for item in self.orderitems.all())
        return total
        
    @property
    def get_total_price(self):
        total = sum(item.get_total for item in self.orderitems.all())
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,related_name='orderitems',null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):
        return self.quantity*self.product.price



class ShippingAddress(models.Model):
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.address
