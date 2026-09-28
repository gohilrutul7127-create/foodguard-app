from django.core.validators import MinValueValidator
from django.db import models
def default_reminder_days(): return [3]
class ReminderSettings(models.Model):
    user=models.OneToOneField('users.User',on_delete=models.CASCADE,related_name='reminder_settings'); reminder_days=models.JSONField(default=default_reminder_days); push_enabled=models.BooleanField(default=True); email_enabled=models.BooleanField(default=True); weekly_digest=models.BooleanField(default=False); updated_at=models.DateTimeField(auto_now=True)
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.reminder_days: raise ValidationError({'reminder_days':'Select at least one reminder interval.'})
        if any(day not in (3,7,15,30) for day in self.reminder_days): raise ValidationError({'reminder_days':'Only 3, 7, 15, and 30 days are supported.'})
        if len(set(self.reminder_days)) != len(self.reminder_days): raise ValidationError({'reminder_days':'Reminder intervals must be unique.'})
class Notification(models.Model):
    class Kind(models.TextChoices): EXPIRY='expiry','Expiry reminder'; SYSTEM='system','System'; SCAN='scan','Scan result'
    user=models.ForeignKey('users.User',on_delete=models.CASCADE,related_name='notifications'); inventory_item=models.ForeignKey('inventory.InventoryItem',on_delete=models.CASCADE,null=True,blank=True,related_name='notifications'); kind=models.CharField(max_length=16,choices=Kind.choices); title=models.CharField(max_length=160); body=models.TextField(); scheduled_for=models.DateTimeField(db_index=True); sent_at=models.DateTimeField(null=True,blank=True); read_at=models.DateTimeField(null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: indexes=[models.Index(fields=['user','read_at','scheduled_for']),models.Index(fields=['scheduled_for','sent_at'])]; constraints=[models.UniqueConstraint(fields=['user','inventory_item','kind','scheduled_for'],name='unique_scheduled_expiry_reminder')]; ordering=['-scheduled_for']
