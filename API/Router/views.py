from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
import django
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Router
from .serializer  import RouterSerializer
import Router as rt
# Create your views here.


#ADMIN
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request):
    """
        Retorna todos as Router. :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id": int,...}..]"</br>  
            RESPONSE CODE 401: Acesso Negado.</br> 
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMIN</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #admin pode ver todas networks
    if user.is_superuser:
        routers = Router.objects.all()
        routersSerializer = RouterSerializer(routers,many=True)
        return Response(routersSerializer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)


#ADMIN
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get(request,id_router):
    """
        Retorna o Router com o Id :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: {"id": int,...}"</br>
            RESPONSE CODE 400: Parametro Invalido.</br>
            RESPONSE CODE 401: Acesso Negado.</br>
            RESPONSE CODE 404: Não Encontrado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>:ADMIN</br>  
    """
    try:
        id_router = int(id_router)
    except Exception as e:
        return Response({"error":"invalid id_router"},status=status.HTTP_400_BAD_REQUEST)
    id_user = request.user.id
    user =  User.objects.get(id=id_user)

    if not user.is_superuser:
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        data = Router.objects.get(id=id_router)
        serializer = RouterSerializer(data, many=False)
        return Response(serializer.data)
    except rt.models.Router.DoesNotExist as e:
        return Response({"erro":"Not found"}, status=status.HTTP_404_NOT_FOUND)


@transaction.atomic
def updateRouter(r):
    r.save()

#ADMIN 
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request):
    """
        Actualiza os dados do Router </br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 201: Actualizado com Sucesso.</br>
            RESPONSE CODE 400: Parâmetros invalidos.</br>
            RESPONSE CODE 401: Acesso Negado.</br> 
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMIN</br>  
    """
    #identificacao
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    if not user.is_superuser :
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    #verificacao de dados da requisicao
    try:
        id_router = int(request.data.get('id'))
        router = Router.objects.get(id=id_router)
    except Exception:
        return Response({"error": "Invalid id"}, status=status.HTTP_400_BAD_REQUEST)
    
    #salvar
    serializer = RouterSerializer(router, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            updateRouter(serializer)
            return Response({"message": "Success"}, status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({'error': 'unsucess'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#ADMIN
@transaction.atomic
def deleteRouter(r):
    r.delete()

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request,id_router_to_delete):
    """
        Apaga o Router com o ID.</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 202: Apagado com sucesso.</br>  
            RESPONSE CODE 401: Acesso Negado.</br>
            RESPONSE CODE 400: O id passado é invalido.</br>    
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMINISTRADOR</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    if user.is_superuser:
        try:
            id_router_to_delete = int(id_router_to_delete)
            router_to_delete = Router.objects.get(id=id_router_to_delete)
        except Exception as e:
            return Response({"error":"invalid id_router"},status=status.HTTP_400_BAD_REQUEST)    
        try:
            deleteRouter(router_to_delete)
            return Response({"message":f"deleted router {id_router_to_delete}"},status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({"error":f"failed to router {id_router_to_delete}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)


class Register(APIView):
    """
        Cadastra um Router8. {"address":"string",....} :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 201: Criado."</br> 
            RESPONSE CODE 400: Atributo invalido.</br> 
            RESPONSE CODE 401: Acesso Negado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMIN</br>  
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  #
    def post(self, request):
        id_user = request.user.id
        user =  User.objects.get(id=id_user)
        if not user.is_superuser :
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
        newRouter = RouterSerializer(data=request.data)
        if newRouter.is_valid():
            newRouter.save()
            return Response({"message":"Router criado com sucesso."},status=status.HTTP_201_CREATED)
        else:
            #retorna o motivo dos dados nao serem validos
             return Response(newRouter.errors, status=status.HTTP_400_BAD_REQUEST)
