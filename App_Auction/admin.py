from django.contrib import admin
from App_Auction.models import ProductModel, ProductLastPrices

# Register your models here.
admin.site.register(ProductModel)
admin.site.register(ProductLastPrices)
