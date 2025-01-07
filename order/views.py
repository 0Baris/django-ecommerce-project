from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Cart, CartItem, DiscountCode, Order
from catalog.models import Product
from django.http import JsonResponse
from django.template.loader import render_to_string
from decimal import Decimal
import uuid
from user.models import UserProfile, Address


## Sepetteki ürünlerin toplam değeri.
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

## Sepet özelliğinin temel fonksiyonu.
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

## İndirim kodu özelliğinin fonksiyonu. --Çok hatalı çalışıyor düzenlemeniz lazım.
@login_required
def apply_discount(request):
    if request.method == 'POST':
        discount_code = request.POST.get('discount_code')
        
        # İndirim kodu yoksa uygula butonu çalışmaz.
        if not discount_code:
            messages.error(request, "İndirim kodu boş olamaz.")
            rendered_messages = render_to_string('partials/_messages.html', {}, request=request)

            return JsonResponse({
                'status': 'error',
                'messages_html': rendered_messages
            })

        user_cart = Cart.objects.get(user=request.user)
        
        # İndirim kodu halihazırda uygulandıysa kullanıcı kodu değiştiremez.
        if user_cart.discount_code:
            messages.error(request, f"İndirim kodu zaten uygulanmış. Kullanılan Kod: {user_cart.discount_code.code}")
            rendered_messages = render_to_string('partials/_messages.html', {}, request=request)

            return JsonResponse({
                'status': 'error',
                'messages_html': rendered_messages
            })

        try:
            # Herhangi bir sorun yoksa indirim kodu burada uygulanır ve oturuma kaydedilir.
            code = DiscountCode.objects.get(code=discount_code, active=True)
            user_cart.discount_code = code
            user_cart.save()

            messages.success(request, "İndirim kodu başarıyla uygulandı.")

            total_price = calculate_total_price(user_cart)
            request.session['total_price'] = str(total_price)
            request.session['discount_code'] = user_cart.discount_code.code

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
            # İndirim kodu geçersizse burada hata mesajı verir.
            messages.error(request, "Geçersiz indirim kodu.")
            rendered_messages = render_to_string('partials/_messages.html', {}, request=request)
            return JsonResponse({
                'status': 'error',
                'messages_html': rendered_messages
            })

    return JsonResponse({'status': 'error', 'message': 'Geçersiz istek.'}, status=400)


## Ürünleri sepete ekleme fonksiyonu.
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
        
        # Sepete ürün eklerken stoğundan fazla ürün eklenemez.
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

        # İşlem sonrası değerlerin yenilenmesi
        cart_items = user_cart.cartitem_set.all()
        total_price = calculate_total_price(user_cart)
        request.session['total_price'] = str(total_price)
        
        rendered_messages = render_to_string('partials/_messages.html', {}, request=request)

        cart_html = render_to_string('cart.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'discount_code': user_cart.discount_code if user_cart.discount_code else None,
        }, request=request)

        return JsonResponse({
            'status': 'success',
            'cart_html': cart_html,
            'rendered_messages': rendered_messages,
            'reload': True  # Sayfanın yenilenmesi gerektiğini belirtir
        })
    
    return JsonResponse({'status': 'error'}, status=400)

## Ürünlerin sepetteki miktarını azaltma fonksiyonu.
@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    # Sepetteki ürünün sayısı 1'den az olamaz, adet azaltarak ürün kaldırılamaz.
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

    # İşlem sonrası değerlerin yenilenmesi.
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

## Ürünlerin sepetteki miktarını arttırma fonksiyonu.
@login_required
def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    product = cart_item.product

    # Stokta yeterli miktarda ürün yoksa burada uyarı verir.
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

## Ürünleri sepetten çıkartma fonksiyonu.
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

## Ödeme aşamasının tamamı bu fonksiyonda bulunur.
@login_required
def checkout(request):
    try:
        # Sipariş ID ve adım bilgisini al
        order_id = request.GET.get('id')
        step = request.GET.get('step', 'info')

        # Eğer sipariş ID mevcut değilse, yeni bir sipariş oluştur
        if not order_id:
            new_order = Order.objects.create(user=request.user)
            checkout_url = reverse('order:checkout') + f'?id={new_order.id}&step=info'
            return redirect(checkout_url)

        # Siparişi al
        order = get_object_or_404(Order, id=order_id, user=request.user)

        # Adres seçimi ve kaydetme
        if step == 'info':
            if request.method == 'POST':
                address_id = request.POST.get('address_id')
                address = get_object_or_404(Address, id=address_id, user=request.user)
                order.address = address
                order.save()
                return redirect(reverse('order:checkout') + f'?id={order.id}&step=payment')
            return render(request, 'info.html', {'order': order})

        # Ödeme işlemi
        elif step == 'payment':
            if request.method == 'POST':
                if request.session.get('payment_completed'):
                    return render(request, 'error.html', {'message': 'Ödeme zaten tamamlandı.'})

                payment_method = request.POST.get('payment_method')
                order.payment_method = payment_method
                order.save()

                request.session['payment_completed'] = True

                return redirect(reverse('order:checkout') + f'?id={order.id}&step=confirmation')

            transaction_id = str(uuid.uuid4())
            request.session['transaction_id'] = transaction_id
            return render(request, 'payment.html', {'order': order, 'transaction_id': transaction_id})

        # Siparişin tamamlanması
        elif step == 'confirmation':
            user_cart = get_object_or_404(Cart, user=request.user)
            total_amount = calculate_total_price(user_cart)
            order.total_amount = total_amount

            for cart_item in user_cart.cartitem_set.all():
                product = cart_item.product
                if cart_item.quantity > product.stock_quantity:
                    messages.error(request, f"Stokta yeterli miktarda {product.name} yok.")
                    return redirect(reverse('order:checkout') + f'?id={order.id}&step=info')

            order.save()

            for cart_item in user_cart.cartitem_set.all():
                product = cart_item.product
                product.stock_quantity -= cart_item.quantity
                product.save()
                order.items.create(product=product.name, quantity=cart_item.quantity, price=product.price)

            if user_cart.discount_code:
                discount_code = user_cart.discount_code
                discount_code.usage += 1
                discount_amount = sum(int(item.product.price) * item.quantity for item in user_cart.cartitem_set.all()) * (Decimal(discount_code.discount) / Decimal('100'))
                discount_code.usage_fee += discount_amount
                discount_code.save()
                order.discount_code = discount_code
                order.save()

            request.session.pop('total_price', None)
            request.session.pop('discount_code', None)

            user_cart.discount_code = None
            user_cart.save()
            user_cart.cartitem_set.all().delete()
            user_cart.save()

            return render(request, 'confirmation.html', {'order': order})

        else:
            return render(request, 'error.html', {'message': 'Geçersiz işlem adımı.'})

    except Exception as e:
        return render(request, 'error.html', {'message': str(e)})