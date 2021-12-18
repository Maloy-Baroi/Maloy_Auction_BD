import datetime

from django.db import models
from django_mysql.models import ListCharField

# Create your models here.
from App_Authentication.models import User

user_length = len(User.objects.all())


class ProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new_bidder = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=200)
    product_photo = models.ImageField(upload_to='product_image')
    minimum_bid_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField(blank=True, null=True)
    product_description = models.TextField()
    auction_end_date = models.DateField()
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)


now = datetime.datetime.now()


class ProductLastPrices(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    price = models.PositiveIntegerField()
    date = models.DateField(auto_now=True)


# user input, Product Name, Product Description, Product Photo, Minimum Bid Price, and Auction End DateTime
