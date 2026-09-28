from django.core.validators import MinValueValidator
from django.db import models
class FoodCategory(models.Model):
    name=models.CharField(max_length=80, unique=True); slug=models.SlugField(unique=True); description=models.TextField(blank=True)
    class Meta: verbose_name_plural='food categories'; ordering=['name']
    def __str__(self): return self.name
class Product(models.Model):
    barcode=models.CharField(max_length=64, unique=True, db_index=True, null=True, blank=True); name=models.CharField(max_length=255, db_index=True); brand=models.CharField(max_length=120, blank=True, db_index=True)
    category=models.ForeignKey(FoodCategory,on_delete=models.PROTECT,related_name='products'); description=models.TextField(blank=True); ingredients=models.TextField(blank=True); storage_instructions=models.TextField(blank=True); serving_size=models.CharField(max_length=80, blank=True); shelf_life_days=models.PositiveIntegerField(null=True,blank=True,validators=[MinValueValidator(1)])
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: indexes=[models.Index(fields=['name','brand']),models.Index(fields=['category','name'])]; ordering=['name']
    def __str__(self): return self.name
class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images'); image=models.ImageField(upload_to='products/%Y/%m/', blank=True); image_url=models.URLField(blank=True); alt_text=models.CharField(max_length=180,blank=True); is_primary=models.BooleanField(default=False); sort_order=models.PositiveSmallIntegerField(default=0)
    class Meta: ordering=['sort_order']; constraints=[models.UniqueConstraint(fields=['product','sort_order'],name='unique_product_image_position')]
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.image and not self.image_url: raise ValidationError('Provide an uploaded image or an image URL.')
