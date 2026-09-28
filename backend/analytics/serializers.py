from rest_framework import serializers
from .models import WasteEvent
class WasteEventSerializer(serializers.ModelSerializer):
    class Meta: model=WasteEvent; fields=('id','inventory_item','quantity','estimated_value','reason','occurred_on','created_at'); read_only_fields=('id','created_at')
