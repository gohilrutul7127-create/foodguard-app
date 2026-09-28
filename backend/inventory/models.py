from django.core.validators import MinValueValidator
from django.db import models
class InventoryItem(models.Model):
    class Storage(models.TextChoices): PANTRY='pantry','Pantry'; FRIDGE='fridge','Fridge'; FREEZER='freezer','Freezer'
    class Status(models.TextChoices): ACTIVE='active','Active'; CONSUMED='consumed','Consumed'; DISCARDED='discarded','Discarded'
    user=models.ForeignKey('users.User',on_delete=models.CASCADE,related_name='inventory_items'); product=models.ForeignKey('products.Product',on_delete=models.PROTECT,related_name='inventory_items')
    quantity=models.DecimalField(max_digits=8,decimal_places=2,default=1,validators=[MinValueValidator(0.01)]); unit=models.CharField(max_length=24,default='item'); purchased_on=models.DateField(null=True,blank=True); expires_on=models.DateField(db_index=True); opened_on=models.DateField(null=True,blank=True); storage_location=models.CharField(max_length=12,choices=Storage.choices,default=Storage.PANTRY); status=models.CharField(max_length=12,choices=Status.choices,default=Status.ACTIVE,db_index=True); actioned_at=models.DateTimeField(null=True,blank=True); notes=models.CharField(max_length=500,blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: indexes=[models.Index(fields=['user','expires_on']),models.Index(fields=['user','storage_location']),models.Index(fields=['user','status','expires_on'])]; ordering=['expires_on']
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.purchased_on and self.expires_on < self.purchased_on: raise ValidationError({'expires_on':'Expiry date cannot be before the purchase date.'})
class ScanHistory(models.Model):
    user=models.ForeignKey('users.User',on_delete=models.CASCADE,related_name='scan_history'); product=models.ForeignKey('products.Product',on_delete=models.SET_NULL,null=True,blank=True,related_name='scans'); barcode=models.CharField(max_length=512,db_index=True); found=models.BooleanField(default=False); extracted_data=models.JSONField(default=dict, blank=True); scanned_at=models.DateTimeField(auto_now_add=True)
    class Meta: indexes=[models.Index(fields=['user','scanned_at'])]; ordering=['-scanned_at']
