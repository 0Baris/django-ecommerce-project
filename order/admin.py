from django.contrib import admin
from .models import DiscountCode, Cart, CartItem, Order, OrderItem

## Sipariş kısmının admin panelini buradan yönetebilirsiniz.

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'usage', 'usage_fee' , 'discount', 'active', 'created_at', 'updated_at')
    search_fields = ('code',)
    list_filter = ('active','usage', 'usage_fee',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'discount_code')
    search_fields = ('user__username', 'discount_code__code')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'get_total_price')
    search_fields = ('order__id', 'product')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('get_total_price',)

    def get_total_price(self, obj):
        return obj.quantity * obj.price if obj.quantity and obj.price else 0
    get_total_price.short_description = 'Total Price'
    can_delete = True

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('new_id', 'user', 'status', 'order_date', 'total_amount')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'user__email')
    inlines = [OrderItemInline]