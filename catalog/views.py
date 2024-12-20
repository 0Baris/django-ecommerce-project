from django.shortcuts import render, get_object_or_404
from .models import Category, Slide, Product

def home(request):
    context = {
        'categories': Category.objects.all()[1:],
        'slides': Slide.objects.all(),
        'products': Product.objects.all()[:12],
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