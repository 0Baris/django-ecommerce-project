from django.shortcuts import render

kategoriler = [
    {'id': 1, 'isim': 'Elektronik', 'slug': 'elektronik'},
    {'id': 2, 'isim': 'Moda', 'slug': 'moda'},
    {'id': 3, 'isim': 'Ev ve Yaşam', 'slug': 'ev-ve-yasam'},
    {'id': 4, 'isim': 'Kitaplar', 'slug': 'kitaplar'},
    {'id': 5, 'isim': 'Spor', 'slug': 'spor'},
    {'id': 6, 'isim': 'Oyuncaklar', 'slug': 'oyuncaklar'},
]

slides = [
    {'id': 0, 'isim': 'İndirim' , 'slug': 'indirim', 'resim': 'static/img/slides1.png'},
    {'id': 1, 'isim': 'Moda' ,'slug': 'moda', 'resim': 'static/img/slides2.png'}
]


def home(request):
    context = {'kategoriler': kategoriler,
               'slides': slides,
               }
    return render(request, 'index.html', context)


def category(request, slug):
    kategori = next(filter(lambda item: item["slug"] == slug, kategoriler))
    context = {'kategori': kategori,
               'kategoriler': kategoriler
               }
    return render(request, 'category.html', context)