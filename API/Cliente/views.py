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
from .models import Cliente
from .serializer  import ClienteSerializer
import Cliente as cl

#verifica se o numero de telefone é valido
def IsphoneNumberValid(cell):
    #Only Mozambican Phone Number Prefix
    if cell == None:
        return False
    try:
        if cell[0:6] in ['+25882','+25883','+25884','+25885','+25886','+25887']:
            if len(cell[6:])==7:
                try:
                    v = int(cell[6:])
                    return True
                except ValueError:
                    return False
    except Exception:
        return False
    return False



#ADMIN
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request):
    """
        Retorna todos Clientes :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id": int,...}..]"</br>  
            RESPONSE CODE 401: Acesso Negado.</br> 
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: ADMINISTRADOR</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    #se a pessoa é superuser, entao vai receber todos os dados dos agentes
    if user.is_superuser:
        data = Cliente.objects.all()
        serializer = ClienteSerializer(data, many=True)
        return Response(serializer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#retorna somente 1 cliente
#CLIENT(id==id_client) 
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getMy(request):
    """
        Retorna os dados do Cliente Autenticado :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: {"id": int,...}"</br>  
            RESPONSE CODE 401: Acesso Negado.</br> 
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: CLIENTES</br>  
    """
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    client = Cliente.objects.filter(id_user=user.id).first()
    if client!=None:
        serializer = ClienteSerializer(client, many=False)
        return Response(serializer.data)
    else:
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#ADMIN
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get(request,id_client):
    """
        Retorna o Cliente com o Id :</br>
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
        id_client = int(id_client)
    except Exception as e:
        return Response({"error":"invalid id_client"},status=status.HTTP_400_BAD_REQUEST)
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    client = Cliente.objects.filter(id_user=user.id).first()
    #verifica se a pessoa é superuser ou se se trata-se do cliente que busca dados sobre a sua conta
    if not user.is_superuser and  client!=None:
        if client.id != id_client:
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        data = Cliente.objects.get(id=id_client)
        serializer = ClienteSerializer(data, many=False)
        return Response(serializer.data)
    except cl.models.Cliente.DoesNotExist as e:
        return Response({"erro":"Not found"}, status=status.HTTP_404_NOT_FOUND)

#transacao para actualizar dados de Clientes
@transaction.atomic
def updateClient(cli):
    cli.save()

#altera os dados de uma agente (somente o numero de telefone)
#CLIENT(id==id_client) 
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request):
    """
        Actualiza os dados do a Cliente Autenticado : {"celular":..}</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 201: Actualizado com Sucesso.</br>
            RESPONSE CODE 400: Parâmetros invalidos.</br>
            RESPONSE CODE 401: Acesso Negado.</br> 
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: CLIENTES</br>  
    """
    #identificacao
    id_user = request.user.id
    user =  User.objects.get(id=id_user)
    cli = Cliente.objects.filter(id_user=user.id).first()
    if cli==None:
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    #verificacao de dados da requisicao
    try:
        id_client = int(request.data.get('id'))
    except Exception:
        return Response({"error": "Invalid id"}, status=status.HTTP_400_BAD_REQUEST)
    if id_client!=cli.id:
        return Response({"error": "Access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    cell = request.data.get('celular')
    #Deve verificar o numero de telefone é valido... ainda é necessario escrever o metodo
    if cell!=None:
        if(not IsphoneNumberValid(cell)):
            return Response({"error":"invalid celular"},status=status.HTTP_400_BAD_REQUEST)
    
    #nao permitir que alguns atributos sejam alguns atributos sejam alterados
    refusedAtt = ['id_user']
    for att in refusedAtt:
        if att in request.data:
            return Response({"error": "invalid operation"}, status=status.HTTP_400_BAD_REQUEST)
        
    #salvar
    serializer = ClienteSerializer(cli, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            updateClient(serializer)
            return Response({"message": "Success"}, status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({'error': 'unsucess'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Create your views here.
#Criar uma conta cliente...
class Register(APIView):
    """
        Cadastra um Cliente. {"celular":"string", "id_user":int} :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 201: Criado."</br> 
            RESPONSE CODE 400: Atributo invalido.</br> 
            RESPONSE CODE 404: Não encontrado.</br>
            RESPONSE CODE 406: Id do usuário não aceite.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: TODOS</br>  
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]  # Permitir acesso a qualquer um para obtenção do token
    def post(self, request):
        
        newClient = ClienteSerializer(data=request.data)
        if newClient.is_valid():
            id_user = request.data.get('id_user')
            cell = request.data.get('celular')
            #verifica se o numero de celular é Valido
            if(not IsphoneNumberValid(cell)):
                return Response({"error":"invalid invalid cell"},status=status.HTTP_400_BAD_REQUEST)
            try:
                user =  User.objects.get(id=id_user)
                if user.is_active:
                    return Response({"erro":"invalid iduser"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                #verifica se o usuario é um administrador, porque administradores nao podem ter contas cliente ou agente
                if user.is_superuser or user.is_staff:
                    return Response({"erro":"invalid iduser"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                user.is_active=True
                user.save()
                newClient.save()
            except django.contrib.auth.models.User.DoesNotExist:
                return Response({"erro":"iduser not found"}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({'username':user.username,"message":"Conta Criada com Sucesso."},status=status.HTTP_201_CREATED)
        else:
            #retorna o motivo dos dados nao serem validos
             return Response(newClient.errors, status=status.HTTP_400_BAD_REQUEST)
