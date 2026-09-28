from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FoodFreshnessDetectionView, InventoryItemViewSet, InventoryStatsView, QRScanView, ScanHistoryViewSet
router=DefaultRouter(); router.register('items',InventoryItemViewSet,basename='inventory-item'); router.register('scans',ScanHistoryViewSet,basename='scan-history'); urlpatterns=[path('stats/',InventoryStatsView.as_view(),name='inventory-stats'),path('scan-qr/',QRScanView.as_view(),name='scan-qr'),path('freshness-detect/',FoodFreshnessDetectionView.as_view(),name='freshness-detect'),*router.urls]
