from django.shortcuts import render

kategoriler = [
    {'id': 1, 'isim': 'Elektronik'},
    {'id': 2, 'isim': 'Moda'},
    {'id': 3, 'isim': 'Ev ve Yaşam'},
    {'id': 4, 'isim': 'Kitaplar'},
    {'id': 5, 'isim': 'Spor'},
    {'id': 6, 'isim': 'Oyuncaklar'},
]

def home(request):
    context = {'kategoriler': kategoriler}
    return render(request, 'index.html', context)

def category(request, id):
    kategori = next(filter(lambda item: item["id"] == id, kategoriler))
    context = {'kategori': kategori}
    return render(request, 'category.html', context)