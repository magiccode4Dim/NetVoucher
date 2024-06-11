from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import * 


app_name = 'Pacote'

urlpatterns = [
    path('register',Register.as_view(),name="RegisterPacote"),
    path('update',update,name="update"),
    path('getall',getAll,name="getall"),
    path('delete/<int:id_pacote_to_delete>',delete,name="delete"),
    path('get/<int:id_pacote>',get,name="get")
]