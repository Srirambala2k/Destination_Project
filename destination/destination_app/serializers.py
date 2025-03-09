# destination_app/serializers.py
from rest_framework import serializers
from .models import Account, Destination, AccountMember, Log, Role

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

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

