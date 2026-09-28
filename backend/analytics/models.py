from django.core.validators import MinValueValidator
from django.db import models
class WasteEvent(models.Model):
    user=models.ForeignKey('users.User',on_delete=models.CASCADE,related_name='waste_events'); inventory_item=models.ForeignKey('inventory.InventoryItem',on_delete=models.SET_NULL,null=True,blank=True); quantity=models.DecimalField(max_digits=8,decimal_places=2,validators=[MinValueValidator(0.01)]); estimated_value=models.DecimalField(max_digits=10,decimal_places=2,default=0,validators=[MinValueValidator(0)]); reason=models.CharField(max_length=120,blank=True); occurred_on=models.DateField(db_index=True); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: indexes=[models.Index(fields=['user','occurred_on'])]
