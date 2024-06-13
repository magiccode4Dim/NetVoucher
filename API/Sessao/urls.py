from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'Sessao'

urlpatterns = [
    path('register',Register.as_view(),name="RegisterSessao"),
    path('update',update,name="update"),
    path('getall',getAll,name="getall"),
    path('delete/<int:id_Sessao_to_delete>',delete,name="delete"),
    path('get/<int:id_Sessao>',get,name="get"),
    path('getbyidcompra/<int:id_compra>',getSessaoByIdCompra,name="getMy"),
]