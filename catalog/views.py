from django.shortcuts import render, get_object_or_404
from .models import Category, Slide, Product

def home(request):
    context = {
        'categories': Category.objects.all(),
        'slides': Slide.objects.all(),
        'products': Product.objects.all()[:12],
    }
    return render(request, 'index.html', context)

def category(request, slug):
    kategori = get_object_or_404(Category, slug=slug)
    products = kategori.products.all()
    context = {
        'kategori': kategori,
        'categories': Category.objects.all(),
        'products': products,
    }
    return render(request, 'category.html', context)

def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product,
        'categories': Category.objects.all(),
    }
    return render(request, 'product.html', context)