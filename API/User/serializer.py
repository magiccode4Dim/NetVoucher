from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','first_name','last_name', 'email', 'password')
    def create(self, validated_data):
        # Extrai a senha dos dados validados
        password = validated_data.pop('password', None)
        #cria o usuario ja desabilitado
        validated_data['is_active'] = False

        # Cria o usuário sem definir a senha ainda
        user = User.objects.create(**validated_data)

        # Insere a senha no objecto, transformando-a em hash
        if password:
            user.set_password(password)
            user.save()

        return user  

