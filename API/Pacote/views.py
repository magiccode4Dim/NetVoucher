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
from .models import Pacote
from .serializer  import PacoteSerializer
import Pacote as pt



#ALL
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request):
    """
        Retorna todos Pacotes:</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: [{"id": int,...}..]"</br>  
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: TODOS</br>  
    """
    data = Pacote.objects.all()
    serializer = PacoteSerializer(data, many=True)
    return Response(serializer.data)
#ALL
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get(request,id_pacote):
    """
        Retorna o Pacote com o Id :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 200: {"id": int,...}"</br>
            RESPONSE CODE 400: Parametro Invalido.</br>
            RESPONSE CODE 404: Não Encontrado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>:ADMIN</br>  
    """
    try:
        id_pacote = int(id_pacote)
    except Exception as e:
        return Response({"error":"invalid id_pacote"},status=status.HTTP_400_BAD_REQUEST)
    try:
        data = Pacote.objects.get(id=id_pacote)
        serializer = PacoteSerializer(data, many=False)
        return Response(serializer.data)
    except pt.models.Pacote.DoesNotExist as e:
        return Response({"erro":"Not found"}, status=status.HTTP_404_NOT_FOUND)

@transaction.atomic
def updatePacote(p):
    p.save()

#ADMIN 
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request):
    """
        Actualiza os dados do a Pacote </br>
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
    if not user.is_superuser :
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    #verificacao de dados da requisicao
    try:
        id_pacote = int(request.data.get('id'))
        pacote = Pacote.objects.get(id=id_pacote)
    except Exception:
        return Response({"error": "Invalid id"}, status=status.HTTP_400_BAD_REQUEST)
    
    #salvar
    serializer = PacoteSerializer(pacote, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            updatePacote(serializer)
            return Response({"message": "Success"}, status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({'error': 'unsucess'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#ADMIN
#transacao para apagar um Pacote
@transaction.atomic
def deletePacote(pacote_to_delete:Pacote):
    pacote_to_delete.delete()

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request,id_pacote_to_delete):
    """
        Apaga o Pacote com o ID.</br>
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
            id_pacote_to_delete = int(id_pacote_to_delete)
            pacote_to_delete = Pacote.objects.get(id=id_pacote_to_delete)
        except Exception as e:
            return Response({"error":"invalid id_pacote"},status=status.HTTP_400_BAD_REQUEST)    
        try:
            deletePacote(pacote_to_delete)
            return Response({"message":f"deleted pacote {id_pacote_to_delete}"},status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({"error":f"failed to delete {id_pacote_to_delete}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#C...
class Register(APIView):
    """
        Cadastra um Pacote. {"nome":"string",....} :</br>
        </br><b>Possiveis Respostas</b>:</br>   
            RESPONSE CODE 201: Criado."</br> 
            RESPONSE CODE 400: Atributo invalido.</br> 
            RESPONSE CODE 401: Acesso Negado.</br>
            RESPONSE CODE 500: Algum erro com o servidor.</br>
        </br><b>PRECISA DE AUTENTICAÇÃO</b>: SIM</br>
        </br><b>QUEM PODE ACESSAR?</b>: TODOS</br>  
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  #
    def post(self, request):
        id_user = request.user.id
        user =  User.objects.get(id=id_user)
        if not user.is_superuser :
            return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
        newPacote = PacoteSerializer(data=request.data)
        if newPacote.is_valid():
            newPacote.save()
            return Response({"message":"Pacote criado com sucesso."},status=status.HTTP_201_CREATED)
        else:
            #retorna o motivo dos dados nao serem validos
             return Response(newPacote.errors, status=status.HTTP_400_BAD_REQUEST)