from rest_framework import serializers
from .models import Sessao

class SessaoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sessao
        fields=('id','id_pacote','id_rooter','id_client','radius_user')