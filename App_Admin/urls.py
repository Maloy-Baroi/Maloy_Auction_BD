from django.urls import path
from App_Admin import views

app_name = 'App_Admin'


urlpatterns = [
    path('', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-authentication/', views.admin_authentication_view, name='admin-authentication'),
    path('logout/', views.logout_view, name='logout'),
    path('products/', views.products_gallery, name='products'),
    path('running-auction/', views.running_auction, name='running-auction'),
    path('product-price-time-series/<product_key>/', views.product_price_time_series, name='product-price-time-series'),
    path('added-ended-chart-product/', views.added_ended_chart_product, name='added-ended-chart-product'),
    path('added-ended-chart/<pk>/', views.added_ended_chart, name='added-ended-chart'),
]
