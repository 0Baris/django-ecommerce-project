from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Cart, CartItem
from catalog.models import Product
from django.http import JsonResponse
from django.template.loader import render_to_string

#Sepet
@login_required
def view_cart(request):
    user_cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = user_cart.cartitem_set.all()
    total_price = sum(int(item.product.price) * item.quantity for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

#Sepete Ekle
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        
        product = Product.objects.get(id=product_id)
        
        user_cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
           

    return redirect('order:view_cart')
    

@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        messages.info(request, "Stokta yeterli miktarda ürün yok.")
    return redirect('order:view_cart')

@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity += 1
        cart_item.save()
    else:
        messages.info(request, "Ürün adeti en az 1 olabilir.")
    return redirect('order:view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, "Ürün başarıyla silindi")
    return redirect('order:view_cart')