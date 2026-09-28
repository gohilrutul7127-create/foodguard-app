from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .models import FoodCategory, Product
from .serializers import FoodCategorySerializer, ProductSerializer
class FoodCategoryViewSet(ModelViewSet):
    queryset=FoodCategory.objects.all(); serializer_class=FoodCategorySerializer; permission_classes=[IsAuthenticatedOrReadOnly]; search_fields=['name','description']; ordering_fields=['name']
class ProductViewSet(ModelViewSet):
    queryset=Product.objects.select_related('category').prefetch_related('images'); serializer_class=ProductSerializer; permission_classes=[IsAuthenticatedOrReadOnly]; filterset_fields=['category','brand']; search_fields=['name','brand','barcode','description']; ordering_fields=['name','brand','created_at']
