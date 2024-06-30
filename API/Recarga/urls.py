from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'Recarga'

urlpatterns = [
    path('generate',Generate.as_view(),name="GenerateRecargas"),
    path('update',update,name="update"),
    path('getall',getAll,name="getall"),
    path('delete/<int:id_router_to_delete>',delete,name="delete"),
    path('get/<int:id_router>',get,name="get")
]