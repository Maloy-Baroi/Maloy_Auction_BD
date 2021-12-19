from django.urls import path
from App_Auction import views

app_name = 'App_Auction'


urlpatterns = [
    path('product-details/<product_key>', views.product_details_view, name='product-details'),
    path('bid-request/', views.bid_start_view, name='bid-request'),
    path('user-participant-auction/', views.user_participant_auctions, name='user-participant-auction'),
    path('my-posted-auctions/', views.my_posted_auctions, name='my-posted-auctions'),
]

