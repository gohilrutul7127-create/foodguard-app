from rest_framework import serializers
from .models import Notification, ReminderSettings
class ReminderSettingsSerializer(serializers.ModelSerializer):
    class Meta: model=ReminderSettings; fields=('reminder_days','push_enabled','email_enabled','weekly_digest','updated_at'); read_only_fields=('updated_at',)
    def validate_reminder_days(self,value):
        if not isinstance(value,list) or not value or any(day not in (3,7,15,30) for day in value) or len(set(value))!=len(value): raise serializers.ValidationError('Choose one or more unique values from 3, 7, 15, and 30 days.')
        return sorted(value,reverse=True)
class NotificationSerializer(serializers.ModelSerializer):
    class Meta: model=Notification; fields=('id','inventory_item','kind','title','body','scheduled_for','sent_at','read_at','created_at'); read_only_fields=('id','sent_at','created_at')
