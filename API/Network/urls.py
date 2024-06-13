from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'Network'

urlpatterns = [
    path('register',Register.as_view(),name="RegisterNetwork"),
    path('update',update,name="update"),
    path('getall',getAll,name="getall"),
    path('delete/<int:id_network_to_delete>',delete,name="delete"),
    path('get/<int:id_network>',get,name="get")
]