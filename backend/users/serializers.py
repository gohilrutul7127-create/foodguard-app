from rest_framework import serializers
from .models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta: model=User; fields=('id','email','first_name','last_name','timezone','date_joined'); read_only_fields=('id','email','date_joined')
