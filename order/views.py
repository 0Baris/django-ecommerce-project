from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Cart, CartItem, DiscountCode
from catalog.models import Product
from django.http import JsonResponse
from django.template.loader import render_to_string
from decimal import Decimal
from user.models import UserProfile 

def calculate_total_price(user_cart):
    subtotal = sum(int(item.product.price) * item.quantity for item in user_cart.cartitem_set.all())
    discount_code = user_cart.discount_code
    if discount_code:
        discount = Decimal(discount_code.discount)
        discount_amount = subtotal * (discount / Decimal('100'))
        total = subtotal - discount_amount
    else:
        total = subtotal
    return total

#Sepet
@login_required
def view_cart(request):
    user_cart = get_object_or_404(Cart, user=request.user)
    total_price = calculate_total_price(user_cart)
    
    request.session['total_price'] = str(total_price)
    request.session['discount_code'] = user_cart.discount_code

    return render(request, 'cart.html', {
        'cart_items': user_cart.cartitem_set.all(),
        'total_price': total_price,
        'discount_code': user_cart.discount_code,
    })

@login_required
def apply_discount(request):
    if request.method == 'POST':
        discount_code = request.POST.get('discount_code')
        user_cart = Cart.objects.get(user=request.user)
        
        try:
            code = DiscountCode.objects.get(code=discount_code, active=True)
            
            # Mevcut bir indirim kodu varsa ve kullanıcı değiştirmek istiyorsa
            if user_cart.discount_code:
                messages.info(request, f"Mevcut indirim kodu {user_cart.discount_code.code} değiştirildi.")
            
            user_cart.discount_code = code
            user_cart.save()

            messages.success(request, "İndirim kodu başarıyla uygulandı.")

            total_price = calculate_total_price(user_cart)
            request.session['total_price'] = str(total_price)
            request.session['discount_code'] = discount_code

            rendered_messages = render_to_string('partials/_messages.html', {}, request=request)

            cart_html = render_to_string('cart.html', {
                'cart_items': user_cart.cartitem_set.all(),
                'total_price': total_price,
                'discount_code': user_cart.discount_code,
            }, request=request)

            return JsonResponse({
                'status': 'success',
                'cart_html': cart_html,
                'messages_html': rendered_messages
            })
        
        except DiscountCode.DoesNotExist:
            messages.error(request, "Geçersiz indirim kodu.")
            rendered_messages = render_to_string('partials/_messages.html', {}, request=request)
            return JsonResponse({
                'status': 'error',
                'messages_html': rendered_messages
            })

    return JsonResponse({'status': 'error', 'message': 'Geçersiz istek.'}, status=400)


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
                messages.error(request, "Stokta yeterli miktarda ürün yok.")
                return JsonResponse({'status': 'error', 'message': 'Stokta yeterli miktarda ürün yok.'}, status=400)
        else:
            if cart_item.quantity > product.stock_quantity:
                messages.error(request, "Stokta yeterli miktarda ürün yok.")
                return JsonResponse({'status': 'error', 'message': 'Stokta yeterli miktarda ürün yok.'}, status=400)

        cart_items = user_cart.cartitem_set.all()
        total_price = calculate_total_price(user_cart)
        request.session['total_price'] = str(total_price)
        
        rendered_messages = render_to_string('partials/_messages.html', {}, request=request)

        cart_html = render_to_string('cart.html', {
            'cart_items': cart_items,
            'total_price': total_price,
        }, request=request)

        return JsonResponse({
            'status': 'success',
            'cart_html': cart_html,
            'rendered_messages': rendered_messages
        })
    
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, "Ürün miktarı azaltıldı.")
    else:
        messages.error(request, "Ürün miktarı 1'den az olamaz. Ürünü kaldırmak için sil butonunu kullanın.")
        rendered_messages = render_to_string('partials/_messages.html', {}, request=request)
        return JsonResponse({
            'status': 'error',
            'messages_html': rendered_messages
        }, status=400)

    user_cart = cart_item.cart
    cart_items = user_cart.cartitem_set.all()
    total_price = calculate_total_price(user_cart)
    request.session['total_price'] = str(total_price)
    
    rendered_messages = render_to_string('partials/_messages.html', {}, request=request)

    cart_html = render_to_string('cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    }, request=request)

    return JsonResponse({
        'status': 'success',
        'cart_html': cart_html,
        'messages_html': rendered_messages
    })

@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    product = cart_item.product

    if cart_item.quantity < product.stock_quantity:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Ürün miktarı artırıldı.")
    else:
        messages.error(request, "Stokta yeterli miktarda ürün yok.")
    
    user_cart = cart_item.cart
    cart_items = user_cart.cartitem_set.all()
    total_price = calculate_total_price(user_cart)
    request.session['total_price'] = str(total_price)
    
    rendered_messages = render_to_string('partials/_messages.html', {}, request=request)

    cart_html = render_to_string('cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    }, request=request)

    return JsonResponse({
        'status': 'success',
        'cart_html': cart_html,
        'messages_html': rendered_messages
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, "Ürün sepetten kaldırıldı.")

    user_cart = cart_item.cart
    cart_items = user_cart.cartitem_set.all()
    total_price = calculate_total_price(user_cart)
    request.session['total_price'] = str(total_price)
    
    rendered_messages = render_to_string('partials/_messages.html', {}, request=request)

    cart_html = render_to_string('cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    }, request=request)

    return JsonResponse({
        'status': 'success',
        'cart_html': cart_html,
        'messages_html': rendered_messages
    })

