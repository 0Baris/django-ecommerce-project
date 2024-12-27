from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Slide, Product, Comment
from django.core.paginator import Paginator
from django.db.models import Q
from order.models import Cart

def home(request):
    search_query = request.GET.get('search', '')
    
    if request.user.is_authenticated:
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = user_cart.cartitem_set.all()
        cart_count = sum(item.quantity for item in cart_items)
    else:
        cart_items = []
        cart_count = 0

    products = Product.objects.filter(is_active=True)
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    
    context = {
        'categories': Category.objects.all()[1:],
        'slides': Slide.objects.select_related('product').all(),
        'products': products[:12],
        'search_query': search_query,
        'cart_items': cart_items,
        'cart_count': cart_count,
    }
    
    return render(request, 'index.html', context)


def category(request, slug):
    kategori = get_object_or_404(Category, slug=slug)
    
    if slug == 'tum-urunler':
        products = Product.objects.filter(is_active=True)
        context = {
            'kategori': kategori,
            'products': products,
        }
    else:
        products = kategori.products.filter(is_active=True)
        context = {
            'kategori': kategori,
            'products': products,
        }
    
    context['categories'] = Category.objects.all()
    
    return render(request, 'category.html', context)


def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product,
        'categories': Category.objects.all(),
        'products': Product.objects.all()
    }
    return render(request, 'product.html', context)
