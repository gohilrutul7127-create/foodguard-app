from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, ReminderSettingsView
router=DefaultRouter(); router.register('',NotificationViewSet,basename='notification'); urlpatterns=[path('settings/',ReminderSettingsView.as_view()),*router.urls]
