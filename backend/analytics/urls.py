from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AnalyticsOverviewView, DashboardAnalyticsView, WasteEventViewSet
router=DefaultRouter(); router.register('waste-events',WasteEventViewSet,basename='waste-event'); urlpatterns=[path('overview/',AnalyticsOverviewView.as_view()),path('dashboard/',DashboardAnalyticsView.as_view()),*router.urls]
