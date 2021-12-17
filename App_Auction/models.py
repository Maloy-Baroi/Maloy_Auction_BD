from django.db import models

# Create your models here.
from App_Authentication.models import User


class ProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new_bidder = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    product_photo = models.ImageField(upload_to='product_image')
    minimum_bid_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField(blank=True, null=True)
    product_description = models.TextField()
    auction_end_date = models.DateField()
    status = models.BooleanField(default=False)
    created = models.DateField(auto_now=True)

# user input, Product Name, Product Description, Product Photo, Minimum Bid Price, and Auction End DateTime
