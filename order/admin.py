from django.contrib import admin
from .models import DiscountCode, Cart, CartItem, Order, OrderItem

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'active', 'created_at', 'updated_at')
    search_fields = ('code',)
    list_filter = ('active',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'discount_code')
    search_fields = ('user__username', 'discount_code__code')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__username', 'product__productName')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'get_total_price')
    search_fields = ('order__id', 'product')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('get_total_price',)
    can_delete = True

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'order_date', 'total_amount')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'user__email')
    inlines = [OrderItemInline]