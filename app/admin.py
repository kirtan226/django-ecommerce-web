from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Customer , Product , Cart , OrderPlaced, CoverImage

# admin.site.register(Customer)
# admin.site.register(Product)
# admin.site.register(Cart)
# admin.site.register(OrderPlaced)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name', 'locality','city','zipcode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','description'
        ,'brand','category','product_image']
    search_fields = ['category']
    list_filter = ['category']

@admin.register(CoverImage)
class CoverImageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'display_order', 'is_active', 'image']
    list_editable = ['display_order', 'is_active']
    search_fields = ['title']
    list_filter = ['is_active']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user_info','customer','product_info','product','quantity','price','ordered_date','status']
    def user_info(self,obj):
        link=reverse('admin:app_customer_change',args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.user)
    def product_info(self,obj):
            link=reverse('admin:app_product_change',args=[obj.product.pk])
            return format_html('<a href="{}">{}</a>',link,obj.product.title)
