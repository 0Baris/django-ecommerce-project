from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Slide, Product, Comment
from django.core.paginator import Paginator
from django.db.models import Q

def home(request):
    search_query = request.GET.get('search', '')
    
    products = Product.objects.filter(is_active=True)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        
        # Simplified context for search results
        context = {
            'categories': Category.objects.all()[1:],
            'products': products,
            'search_query': search_query,
        }
    else:
        # Full context for homepage
        context = {
            'categories': Category.objects.all()[1:],
            'slides': Slide.objects.select_related('product').all(),
            'products': products[:12],  # Limit to 12 products on homepage
            'search_query': search_query,
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
