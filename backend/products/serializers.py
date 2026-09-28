from rest_framework import serializers
from .models import FoodCategory, Product, ProductImage
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta: model=ProductImage; fields=('id','image','image_url','alt_text','is_primary','sort_order')
class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta: model=FoodCategory; fields=('id','name','slug','description')
class ProductSerializer(serializers.ModelSerializer):
    category=FoodCategorySerializer(read_only=True); category_id=serializers.PrimaryKeyRelatedField(source='category',queryset=FoodCategory.objects.all(),write_only=True); images=ProductImageSerializer(many=True,read_only=True)
    class Meta: model=Product; fields=('id','barcode','name','brand','category','category_id','description','ingredients','storage_instructions','serving_size','shelf_life_days','images','created_at','updated_at'); read_only_fields=('id','created_at','updated_at')
