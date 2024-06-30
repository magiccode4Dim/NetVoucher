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
from .models import Recarga
from .serializer  import RecargaSerializer
import Recarga as rt
from .generateCode import generate_unique_code_byrandom
from Cliente.models import Cliente
# Create your views here.


#ADMIN
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAll(request):
    """
        Retorna todos as Recarga. :</br>
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
        Recargas = Recarga.objects.all()
        RecargasSerializer = RecargaSerializer(Recargas,many=True)
        return Response(RecargasSerializer.data)
    return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)


#ADMIN
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get(request,id_Recarga):
    """
        Retorna o Recarga com o Id :</br>
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
        id_Recarga = int(id_Recarga)
    except Exception as e:
        return Response({"error":"invalid id_Recarga"},status=status.HTTP_400_BAD_REQUEST)
    id_user = request.user.id
    user =  User.objects.get(id=id_user)

    if not user.is_superuser:
        return Response({"erro":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        data = Recarga.objects.get(id=id_Recarga)
        serializer = RecargaSerializer(data, many=False)
        return Response(serializer.data)
    except rt.models.Recarga.DoesNotExist as e:
        return Response({"erro":"Not found"}, status=status.HTTP_404_NOT_FOUND)


@transaction.atomic
def updateRecarga(r):
    r.save()

#ADMIN 
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request):
    """
        Actualiza os dados do Recarga </br>
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
        id_Recarga = int(request.data.get('id'))
        Recarga = Recarga.objects.get(id=id_Recarga)
    except Exception:
        return Response({"error": "Invalid id"}, status=status.HTTP_400_BAD_REQUEST)
    
    #salvar
    serializer = RecargaSerializer(Recarga, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            updateRecarga(serializer)
            return Response({"message": "Success"}, status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({'error': 'unsucess'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#ADMIN
@transaction.atomic
def deleteRecarga(r):
    r.delete()

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request,id_Recarga_to_delete):
    """
        Apaga o Recarga com o ID.</br>
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
            id_Recarga_to_delete = int(id_Recarga_to_delete)
            Recarga_to_delete = Recarga.objects.get(id=id_Recarga_to_delete)
        except Exception as e:
            return Response({"error":"invalid id_Recarga"},status=status.HTTP_400_BAD_REQUEST)    
        try:
            deleteRecarga(Recarga_to_delete)
            return Response({"message":f"deleted Recarga {id_Recarga_to_delete}"},status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({"error":f"failed to Recarga {id_Recarga_to_delete}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error":"access denied"}, status=status.HTTP_401_UNAUTHORIZED)

#gera uma quantidade de recargas
class Generate(APIView):
    """
        Gera um quantidade de recargas de um pacote, a um preco. {"n":int,"preco":"string",....} :</br>
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
        data = request.data
        try:
            n = int(data.pop("n"))
        except Exception:
            return Response({"erro":"atribute n not found"}, status=status.HTTP_400_BAD_REQUEST)
        for i in range(n):
            data["code"] = generate_unique_code_byrandom(Recarga.objects.filter(is_valid=True))
            newRecarga = RecargaSerializer(data=data)
            if newRecarga.is_valid():
                newRecarga.save()
            else:
                #retorna o motivo dos dados nao serem validos
                return Response(newRecarga.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":f" {n} Recargas Geradas com Sucesso."},status=status.HTTP_201_CREATED)
