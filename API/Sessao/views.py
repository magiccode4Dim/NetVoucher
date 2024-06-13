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
from .models import Sessao
from Cliente.models import Cliente
from Compra.models import Compra
from .serializer  import SessaoSerializer
import Sessao as nk
import Compra as cpr
# Create your views here.

#ADMIN
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request):
    """
        Retorna todos as Sessao. :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id": int,...}..]"</br>  
            RESPONSE CODE 401: Acesso Negado.</br> 
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMIN</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #admin pode ver todas Sessaos
    if user.is_superuser:
        Sessaos = Sessao.objects.all()
        SessaosSerializer = SessaoSerializer(Sessaos,many=True)
        return Response(SessaosSerializer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#ADMIN
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get(request,id_Sessao):
    """
        Retorna o Sessao com o Id :</br>
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
        id_Sessao = int(id_Sessao)
    except Exception as e:
        return Response({"error":"invalid id_Sessao"},status=status.HTTP_400_BAD_REQUEST)
    id_user = request.user.id
    user =  User.objects.get(id=id_user)

    if not user.is_superuser:
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        data = Sessao.objects.get(id=id_Sessao)
        serializer = SessaoSerializer(data, many=False)
        return Response(serializer.data)
    except nk.models.Sessao.DoesNotExist as e:
        return Response({"erro":"Not found"}, status=status.HTTP_404_NOT_FOUND)

#retorna as sessoes de uma.determinada compra
#CLIENT(id==id_client) 
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getSessaoByIdCompra(request, id_compra):
    """
        Retorna os dados da sessao de uma determinada compra :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id": int,...}...]"</br>  
            RESPONSE CODE 401: Acesso Negado.</br> 
            RESPONSE CODE 404: nao encontrado.</br> 
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: CLIENTES</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    client = Cliente.objects.filter(id_user=user.id).first()
    try:
        id_compra = int(id_compra)
    except Exception as e:
        return Response({"error":"invalid id_compra"},status=status.HTTP_400_BAD_REQUEST)
    if client!=None:
        try:
            compra = Compra.objects.get(id=id_compra, id_cliente=client.id)
        except cpr.models.Compra.DoesNotExist as e:
            return Response({"erro":"Not found"}, status=status.HTTP_404_NOT_FOUND)
        sessoes = Sessao.objects.filter(id_compra=compra.id)
        if sessoes:
            serializer = SessaoSerializer(sessoes, many=True)
            return Response(serializer.data)
        else:
            return Response({"erro":"Not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

@transaction.atomic
def updateSessao(n):
    n.save()

#ADMIN-SYSTEM
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request):
    """
        Actualiza os dados do Sessao </br>
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
        id_Sessao = int(request.data.get('id'))
        sessao = Sessao.objects.get(id=id_Sessao)
        print(Sessao)
    except Exception:
        return Response({"error": "Invalid id"}, status=status.HTTP_400_BAD_REQUEST)
    
    #salvar
    serializer = SessaoSerializer(sessao, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            updateSessao(serializer)
            return Response({"message": "Success"}, status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({'error': 'unsucess'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#ADMIN-SYSTEM
@transaction.atomic
def deleteSessao(Sessao):
    Sessao.delete()

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request,id_Sessao_to_delete):
    """
        Apaga o Sessao com o ID.</br>
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
            id_Sessao_to_delete = int(id_Sessao_to_delete)
            Sessao_to_delete = Sessao.objects.get(id=id_Sessao_to_delete)
        except Exception as e:
            return Response({"error":"invalid id_Sessao"},status=status.HTTP_400_BAD_REQUEST)    
        try:
            deleteSessao(Sessao_to_delete)
            return Response({"message":f"deleted Sessao {id_Sessao_to_delete}"},status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({"error":f"failed to Sessao {id_Sessao_to_delete}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#ADMIN-SYSTEM
class Register(APIView):
    """
        Cadastra um Sessao. {"address":"string",....} :</br>
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
        newSessao = SessaoSerializer(data=request.data)
        if newSessao.is_valid():
            newSessao.save()
            return Response({"message":"Sessao criado com sucesso."},status=status.HTTP_201_CREATED)
        else:
            #retorna o motivo dos dados nao serem validos
             return Response(newSessao.errors, status=status.HTTP_400_BAD_REQUEST)





