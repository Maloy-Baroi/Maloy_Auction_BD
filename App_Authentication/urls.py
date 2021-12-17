from django.urls import path
from App_Authentication import views
app_name = 'App_Authentication'


urlpatterns = [
    path('authentication/', views.authentication_view, name='authentication'),
    path('logout/', views.logout_view, name='logout'),
]

