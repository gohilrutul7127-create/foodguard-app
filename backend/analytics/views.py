from datetime import timedelta
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils.timezone import localdate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import WasteEvent
from .serializers import WasteEventSerializer
class WasteEventViewSet(ModelViewSet):
    serializer_class=WasteEventSerializer; filterset_fields=['occurred_on']; ordering_fields=['occurred_on','estimated_value']
    def get_queryset(self): return WasteEvent.objects.filter(user=self.request.user)
    def perform_create(self,serializer): serializer.save(user=self.request.user)
class DashboardAnalyticsView(APIView):
    def get(self,request):
        items=request.user.inventory_items
        return Response({'inventory_count':items.count(),'expiring_soon':items.filter(expires_on__lte=__import__('django.utils.timezone',fromlist=['localdate']).localdate()+__import__('datetime').timedelta(days=7)).count(),'waste':WasteEvent.objects.filter(user=request.user).aggregate(total_value=Sum('estimated_value'),total_events=Count('id'))})
class AnalyticsOverviewView(APIView):
    def get(self,request):
        from inventory.models import InventoryItem
        today=localdate(); soon=today+timedelta(days=7)
        active=InventoryItem.objects.filter(user=request.user,status=InventoryItem.Status.ACTIVE)
        categories=list(active.values('product__category__name').annotate(value=Count('id')).order_by('-value'))
        category_data=[{'name':row['product__category__name'] or 'Uncategorized','value':row['value']} for row in categories]
        expiry_trends=[{'name':'Expired','value':active.filter(expires_on__lt=today).count()},{'name':'0–3 days','value':active.filter(expires_on__gte=today,expires_on__lte=today+timedelta(days=3)).count()},{'name':'4–7 days','value':active.filter(expires_on__gt=today+timedelta(days=3),expires_on__lte=soon).count()},{'name':'Safe','value':active.filter(expires_on__gt=soon).count()}]
        cutoff=today.replace(day=1)-timedelta(days=150)
        monthly=active.filter(created_at__date__gte=cutoff).annotate(month=TruncMonth('created_at')).values('month').annotate(products=Count('id')).order_by('month')
        monthly_data=[{'month':row['month'].strftime('%b'),'products':row['products']} for row in monthly]
        waste=WasteEvent.objects.filter(user=request.user).aggregate(discarded_value=Sum('estimated_value'),discarded_items=Count('id'))
        consumed=InventoryItem.objects.filter(user=request.user,status=InventoryItem.Status.CONSUMED).count()
        discarded=InventoryItem.objects.filter(user=request.user,status=InventoryItem.Status.DISCARDED).count()
        return Response({'stats':{'total_products':active.count(),'safe_products':active.filter(expires_on__gt=soon).count(),'expiring_products':active.filter(expires_on__gte=today,expires_on__lte=soon).count(),'expired_products':active.filter(expires_on__lt=today).count()},'categories':category_data,'expiry_trends':expiry_trends,'monthly_additions':monthly_data,'waste_reduction':{'consumed_products':consumed,'discarded_products':discarded,'waste_events':waste['discarded_items'] or 0,'waste_value':float(waste['discarded_value'] or 0),'recovery_rate':round((consumed/(consumed+discarded)*100) if consumed+discarded else 0,1)}})
