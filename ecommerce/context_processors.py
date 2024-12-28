from order.models import Cart
from catalog.models import Category

def cart_context(request):
    if request.user.is_authenticated:
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = user_cart.cartitem_set.all()
        cart_count = sum(item.quantity for item in cart_items)
        total_price = sum(int(item.product.price) * item.quantity for item in cart_items)

    else:
        cart_items = []
        cart_count = 0
        total_price = 0

    return {
        'cart_items': cart_items,
        'cart_count': cart_count,
        'total_price': total_price,

    }


def category_context(request):
    categories = Category.objects.all()
    return {
        'categories': categories,
    }