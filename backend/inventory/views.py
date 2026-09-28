from datetime import timedelta
from django.db import transaction
from django.db.models import Count
from django.utils.timezone import localdate, now
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import InventoryItem, ScanHistory
from .serializers import InventoryItemSerializer, ScanHistorySerializer
from .services import QRDecodeError, decode_qr, parse_product_payload
class InventoryItemViewSet(ModelViewSet):
    serializer_class=InventoryItemSerializer; filterset_fields=['storage_location','product','status']; search_fields=['product__name','product__brand','notes']; ordering_fields=['expires_on','created_at','updated_at','quantity']
    def get_queryset(self):
        query=InventoryItem.objects.filter(user=self.request.user).select_related('product','product__category')
        category=self.request.query_params.get('expiry_category')
        if category=='safe': query=query.filter(expires_on__gt=localdate()+timedelta(days=7))
        elif category=='expiring_soon': query=query.filter(expires_on__gte=localdate(),expires_on__lte=localdate()+timedelta(days=7))
        elif category=='expired': query=query.filter(expires_on__lt=localdate())
        return query
    def perform_create(self, serializer): serializer.save(user=self.request.user)
    @action(detail=True,methods=['post'])
    def consume(self,request,pk=None):
        item=self.get_object(); item.status=InventoryItem.Status.CONSUMED; item.actioned_at=now(); item.save(update_fields=['status','actioned_at','updated_at']); return Response(self.get_serializer(item).data)
    @action(detail=True,methods=['post'])
    def discard(self,request,pk=None):
        item=self.get_object(); item.status=InventoryItem.Status.DISCARDED; item.actioned_at=now(); item.save(update_fields=['status','actioned_at','updated_at']); return Response(self.get_serializer(item).data)
class InventoryStatsView(APIView):
    def get(self,request):
        items=InventoryItem.objects.filter(user=request.user,status=InventoryItem.Status.ACTIVE)
        today=localdate(); soon=today+timedelta(days=7)
        return Response({'total_products':items.count(),'safe_products':items.filter(expires_on__gt=soon).count(),'expiring_products':items.filter(expires_on__gte=today,expires_on__lte=soon).count(),'expired_products':items.filter(expires_on__lt=today).count()})
class ScanHistoryViewSet(ReadOnlyModelViewSet):
    serializer_class=ScanHistorySerializer; filterset_fields=['found']; ordering_fields=['scanned_at']
    def get_queryset(self): return ScanHistory.objects.filter(user=self.request.user).select_related('product')
class QRScanView(APIView):
    parser_classes=[MultiPartParser]
    @transaction.atomic
    def post(self,request):
        image=request.FILES.get('image')
        if not image: return Response({'detail':'Attach a QR image in the image field.'},status=status.HTTP_400_BAD_REQUEST)
        try: data=parse_product_payload(decode_qr(image))
        except QRDecodeError as error: return Response({'detail':str(error),'code':'invalid_qr'},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        from products.models import FoodCategory, Product
        product=Product.objects.filter(barcode=data['barcode']).select_related('category').first()
        if not product and data['name']:
            category,_=FoodCategory.objects.get_or_create(slug='uncategorized',defaults={'name':'Uncategorized'})
            product=Product.objects.create(barcode=data['barcode'],name=data['name'],brand=data['brand'],category=category,ingredients=data['ingredients'],storage_instructions=data['storage_instructions'])
        if product:
            data.update({'name':product.name,'brand':product.brand,'ingredients':product.ingredients or data['ingredients'],'storage_instructions':product.storage_instructions or data['storage_instructions']})
        history=ScanHistory.objects.create(user=request.user,product=product,barcode=data['barcode'],found=bool(product),extracted_data=data)
        return Response({'product':data,'product_id':product.id if product else None,'scan_id':history.id},status=status.HTTP_200_OK)

class FoodFreshnessDetectionView(APIView):
    parser_classes=[MultiPartParser]
    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({'detail': 'Please upload an image file in the "image" field.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            from .freshness import analyze_food_freshness
            result = analyze_food_freshness(image.read())
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': f'Error analyzing image freshness: {str(e)}'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

