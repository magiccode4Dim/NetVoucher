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
from .models import Compra
from Cliente.models import Cliente
from .serializer  import CompraSerializer
import Compra as cp
import Cliente as cl
# Create your views here.

#ADMIN, CLIENT
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request):
    """
        Retorna todos as Compras. :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id": int,...}..]"</br>  
            RESPONSE CODE 401: Acesso Negado.</br> 
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMIN, CLIENT</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #o cliente pode ver somente as compras dele
    cli = Cliente.objects.filter(id_user=user.id).first()
    if cli:
        compras = Compra.objects.filter(id_cliente=cli.id)
        comprasSerializer = CompraSerializer(compras,many=True)
        return Response(comprasSerializer.data)
    #admin pode ver todas compras
    if user.is_superuser:
        compras = Compra.objects.all()
        comprasSerializer = CompraSerializer(compras,many=True)
        return Response(comprasSerializer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)


#ADMIN, CLIENT
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get(request,id_compra):
    """
        Retorna todos as Compras. :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id": int,...}..]"</br>  
            RESPONSE CODE 401: Acesso Negado.</br> 
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMIN, CLIENT</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #o cliente pode ver somente as compras dele
    cli = Cliente.objects.filter(id_user=user.id).first()
    try:
        if cli:
            compra = Compra.objects.get(id_cliente=cli.id,id=id_compra)
            compraSerializer = CompraSerializer(compra,many=False)
            return Response(compraSerializer.data)
        #admin pode ver todas compras
        if user.is_superuser:
            compra = Compra.objects.get(id=id_compra)
            compraSerializer = CompraSerializer(compra,many=False)
            return Response(compraSerializer.data)
    except cp.models.Compra.DoesNotExist:
        return Response({"erro":"not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#CLIENT
class Register(APIView):
    """
        Cadastra um Compra</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 201:{"message":"..",...} "</br>
            RESPONSE CODE 404: Não encontrado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: CLIENTES</br>  
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Permitir acesso a apenas os que estiverem autenticados
    def post(self, request):
        user_token = request.auth
        #PEGAR O ID DO USUARIO COM ESSE TOKEN
        id_user = request.user.id
        #VERIFICAR SE O USUARIO É UM CLIENTE
        try:
            cli = Cliente.objects.get(id_user=id_user)
        except cl.models.Cliente.DoesNotExist:
            return Response({"erro":"client not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data["id_cliente"] = cli.id
        newCompra =  CompraSerializer(data=data)
        if newCompra.is_valid():
            #SISTEMA DE PAGAMENTO
            newCompra.save()
            return Response({"message":"Compra Efectuada com Sucesso."},status=status.HTTP_201_CREATED)
        else:
            return Response(newConta.errors, status=status.HTTP_400_BAD_REQUEST)
