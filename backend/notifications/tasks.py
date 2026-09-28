from datetime import timedelta
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import localdate, make_aware
from inventory.models import InventoryItem
from .models import Notification, ReminderSettings

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries':3})
def send_daily_expiry_reminders(self):
    today=localdate(); created=0
    active=InventoryItem.objects.filter(status=InventoryItem.Status.ACTIVE).select_related('user','product')
    for item in active.iterator():
        days=(item.expires_on-today).days
        if days not in (3,7,15,30): continue
        prefs,_=ReminderSettings.objects.get_or_create(user=item.user,defaults={'reminder_days':[3]})
        if days not in prefs.reminder_days: continue
        scheduled_for=make_aware(__import__('datetime').datetime.combine(today,__import__('datetime').time.min))
        title=f'{item.product.name} expires in {days} days'
        body=f'Use {item.product.name} by {item.expires_on:%b %d, %Y}. Storage: {item.storage_location}.'
        notification,was_created=Notification.objects.get_or_create(user=item.user,inventory_item=item,kind=Notification.Kind.EXPIRY,scheduled_for=scheduled_for,defaults={'title':title,'body':body})
        if not was_created: continue
        created+=1
        if prefs.email_enabled:
            send_mail(title,body,settings.DEFAULT_FROM_EMAIL,[item.user.email],fail_silently=False)
        notification.sent_at=__import__('django.utils.timezone',fromlist=['now']).now(); notification.save(update_fields=['sent_at'])
    return {'created':created,'checked_on':str(today)}
