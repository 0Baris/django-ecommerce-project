from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Slide, Product, Comment
from django.core.paginator import Paginator
from django.db.models import Q
from order.models import Cart

## Anasayfa fonksiyonu
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

## Kategori fonksiyonu
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

## Ürün fonksiyonu
def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product,
        'categories': Category.objects.all(),
        'products': Product.objects.all(),
        'comments': Comment.objects.filter(product=product),
    }
    return render(request, 'product.html', context)

def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        text = request.POST.get('text')
        rating = request.POST.get('rating')
        
        if text and rating:
            Comment.objects.create(
                product=product,
                user=request.user,
                text=text,
                rating=rating
            )
            product.comment_count += 1
            product.total_stars += int(rating)
            product.save()
            return redirect('catalog:product', slug=slug)
    
    return render(request, 'add_review.html', {'product': product})