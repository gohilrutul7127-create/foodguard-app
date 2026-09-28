from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Notification, ReminderSettings
from .serializers import NotificationSerializer, ReminderSettingsSerializer
class ReminderSettingsView(RetrieveUpdateAPIView):
    serializer_class=ReminderSettingsSerializer
    def get_object(self): return ReminderSettings.objects.get_or_create(user=self.request.user,defaults={'reminder_days':[3]})[0]
class NotificationViewSet(ModelViewSet):
    serializer_class=NotificationSerializer; http_method_names=['get','head','options','patch']
    filterset_fields=['kind','read_at']; search_fields=['title','body']; ordering_fields=['scheduled_for','created_at']
    def get_queryset(self): return Notification.objects.filter(user=self.request.user).select_related('inventory_item')
