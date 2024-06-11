from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'Compra'

urlpatterns = [
    path('register',Register.as_view(),name="RegisterCompra"),
    path('getall',getAll,name="getall"),
    path('get/<int:id_compra>',get,name="get")   
]