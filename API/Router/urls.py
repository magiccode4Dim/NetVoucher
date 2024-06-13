from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'Router'

urlpatterns = [
    path('register',Register.as_view(),name="RegisterRouter"),
    path('update',update,name="update"),
    path('getall',getAll,name="getall"),
    path('delete/<int:id_router_to_delete>',delete,name="delete"),
    path('get/<int:id_router>',get,name="get")
]