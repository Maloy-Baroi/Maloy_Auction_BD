from django.urls import path
from App_Auction import views

app_name = 'App_Auction'


urlpatterns = [
    path('product-details/<product_key>', views.product_details_view, name='product-details'),
    path('bid-request/', views.bid_start_view, name='bid-request'),
]


