from rest_framework import serializers
from .models import Item
from django.contrib.auth.models import User
#serializers take the python model and turn it into JSON

# User Serializer
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'