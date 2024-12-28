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

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
        
        if not created:
            if cart_item.quantity < product.stock_quantity:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.success(request, "Stokta yeterli miktarda ürün yok.")
                return JsonResponse({'status': 'error', 'message': 'Stokta yeterli miktarda ürün yok.'}, status=400)
        else:
            if cart_item.quantity > product.stock_quantity:
                messages.success(request, "Stokta yeterli miktarda ürün yok.")
                return JsonResponse({'status': 'error', 'message': 'Stokta yeterli miktarda ürün yok.'}, status=400)

        cart_items = user_cart.cartitem_set.all()
        total_price = sum(int(item.product.price) * item.quantity for item in cart_items)
        
        cart_html = render_to_string('cart.html', {
            'cart_items': cart_items,
            'total_price': total_price,
        }, request=request)

        return JsonResponse({
            'status': 'success',
            'cart_html': cart_html
        })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        messages.success(request, "Ürün miktarı 1'den az olamaz. Ürünü kaldırmak için sil butonunu kullanın.")
        return JsonResponse({'status': 'error', 'message': "Ürün miktarı 1'den az olamaz. Ürünü kaldırmak için sil butonunu kullanın."}, status=400)

    user_cart = cart_item.cart
    cart_items = user_cart.cartitem_set.all()
    total_price = sum(int(item.product.price) * item.quantity for item in cart_items)
    
    cart_html = render_to_string('cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    }, request=request)

    return JsonResponse({
        'status': 'success',
        'cart_html': cart_html
    })

@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    product = cart_item.product

    if cart_item.quantity < product.stock_quantity:
        cart_item.quantity += 1
        cart_item.save()
    else:
        messages.success(request, "Stokta yeterli miktarda ürün yok.")
    
    user_cart = cart_item.cart
    cart_items = user_cart.cartitem_set.all()
    total_price = sum(int(item.product.price) * item.quantity for item in cart_items)
    
    cart_html = render_to_string('cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    }, request=request)

    return JsonResponse({
        'status': 'success',
        'cart_html': cart_html
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()

    user_cart = cart_item.cart
    cart_items = user_cart.cartitem_set.all()
    total_price = sum(int(item.product.price) * item.quantity for item in cart_items)
    
    cart_html = render_to_string('cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    }, request=request)

    return JsonResponse({
        'status': 'success',
        'cart_html': cart_html
    })