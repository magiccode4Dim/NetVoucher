from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'Cliente'

urlpatterns = [
    path('register',Register.as_view(),name="RegisterClient"),
    path('update',update,name="update"),
    path('getall',getAll,name="getall"),
    path('get/<int:id_client>',get,name="get"),
    path('get',getMy,name="getMy"),
]