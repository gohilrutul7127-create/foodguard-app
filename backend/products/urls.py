from rest_framework.routers import DefaultRouter
from .views import FoodCategoryViewSet, ProductViewSet
router=DefaultRouter(); router.register('categories',FoodCategoryViewSet); router.register('',ProductViewSet,basename='product'); urlpatterns=router.urls
