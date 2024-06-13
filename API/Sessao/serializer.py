from rest_framework import serializers
from .models import Sessao

class SessaoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sessao
        fields=('id','id_rooter','id_compra','radius_user','device','expira_em')