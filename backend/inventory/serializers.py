from rest_framework import serializers
from .models import InventoryItem, ScanHistory
class InventoryItemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.name',read_only=True)
    expiry_category=serializers.SerializerMethodField()
    class Meta: model=InventoryItem; fields=('id','product','product_name','quantity','unit','purchased_on','expires_on','opened_on','storage_location','status','actioned_at','expiry_category','notes','created_at','updated_at'); read_only_fields=('id','status','actioned_at','expiry_category','created_at','updated_at')
    def get_expiry_category(self,obj):
        from django.utils.timezone import localdate
        if obj.expires_on < localdate(): return 'expired'
        if obj.expires_on <= localdate()+__import__('datetime').timedelta(days=7): return 'expiring_soon'
        return 'safe'
    def validate(self, attrs):
        purchased=attrs.get('purchased_on',getattr(self.instance,'purchased_on',None)); expires=attrs.get('expires_on',getattr(self.instance,'expires_on',None))
        if purchased and expires and expires<purchased: raise serializers.ValidationError({'expires_on':'Expiry date cannot be before purchase date.'})
        return attrs
class ScanHistorySerializer(serializers.ModelSerializer):
    class Meta: model=ScanHistory; fields=('id','barcode','product','found','extracted_data','scanned_at'); read_only_fields=('id','scanned_at')
