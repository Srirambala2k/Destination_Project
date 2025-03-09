# destination_app/serializers.py
from rest_framework import serializers
from .models import Account, Destination, AccountMember, Log, Role
from django.contrib.auth import get_user_model

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'

class AccountMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountMember
        fields = '__all__'

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'

class Role_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


User = get_user_model()  

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_name']  

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()  # Nesting the RoleSerializer to represent the role of a user

    class Meta:
        model = User  
        fields = ['email','password']  

