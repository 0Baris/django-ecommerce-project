from django.shortcuts import render

kategoriler = [
    {'id': 1, 'name': 'Elektronik', 'slug': 'elektronik'},
    {'id': 2, 'name': 'Moda', 'slug': 'moda'},
    {'id': 3, 'name': 'Ev ve Yaşam', 'slug': 'ev-ve-yasam'},
    {'id': 4, 'name': 'Kitaplar', 'slug': 'kitaplar'},
    {'id': 5, 'name': 'Spor', 'slug': 'spor'},
    {'id': 6, 'name': 'Oyuncaklar', 'slug': 'oyuncaklar'},
]

slides = [
    {'id': 0, 'name': 'İndirim' , 'slug': 'indirim', 'resim': 'static/img/slides1.png'},
    {'id': 1, 'name': 'Moda' ,'slug': 'moda', 'resim': 'static/img/slides2.png'},
    {'id': 2, 'name': 'Moda' ,'slug': 'moda', 'resim': 'static/img/slides2.png'}
]

products = [
    {'id': 0, 'name': 'Razer Basilisk V3 Gaming Mouse','price': 1000, 'slug': 'razer-basilisk-v3-gaming-mouse', 'resim': 'static/img/products/razer_basilisk.jpg'},
    {'id': 1, 'name': 'INTEL ARC B580', 'price': 2000, 'slug': 'intel-arc-b580', 'resim': 'static/img/products/intel_ekrankarti.jpg'},
    {'id': 2, 'name': 'GOODRAM 8GB 3600MHz DDR4 Ram', 'price': 3000, 'slug': 'goodram-8gb-3600mhz-ddr4-ram', 'resim': 'static/img/products/8gb_ram.jpg'},
    {'id': 3, 'name': 'GOODRAM 8GB 3600MHz DDR4 Ram', 'price': 3000, 'slug': 'goodram-8gb-3600mhz-ddr4-ram', 'resim': 'static/img/products/8gb_ram.jpg'},
    {'id': 5, 'name': 'GOODRAM 8GB 3600MHz DDR4 Ram', 'price': 3000, 'slug': 'goodram-8gb-3600mhz-ddr4-ram', 'resim': 'static/img/products/8gb_ram.jpg'},
    {'id': 6, 'name': 'GOODRAM 8GB 3600MHz DDR4 Ram', 'price': 3000, 'slug': 'goodram-8gb-3600mhz-ddr4-ram', 'resim': 'static/img/products/8gb_ram.jpg'},
    {'id': 7, 'name': 'GOODRAM 8GB 3600MHz DDR4 Ram', 'price': 3000, 'slug': 'goodram-8gb-3600mhz-ddr4-ram', 'resim': 'static/img/products/8gb_ram.jpg'},
    {'id': 8, 'name': 'GOODRAM 8GB 3600MHz DDR4 Ram', 'price': 3000, 'slug': 'goodram-8gb-3600mhz-ddr4-ram', 'resim': 'static/img/products/8gb_ram.jpg'},
    {'id': 9, 'name': 'GOODRAM 8GB 3600MHz DDR4 Ram', 'price': 3000, 'slug': 'goodram-8gb-3600mhz-ddr4-ram', 'resim': 'static/img/products/8gb_ram.jpg'},
    {'id': 10, 'name': 'GOODRAM 8GB 3600MHz DDR4 Ram', 'price': 3000, 'slug': 'goodram-8gb-3600mhz-ddr4-ram', 'resim': 'static/img/products/8gb_ram.jpg'},
    {'id': 11, 'name': 'GOODRAM 8GB 3600MHz DDR4 Ram', 'price': 3000, 'slug': 'goodram-8gb-3600mhz-ddr4-ram', 'resim': 'static/img/products/8gb_ram.jpg'},
    {'id': 12, 'name': 'GOODRAM 8GB 3600MHz DDR4 Ram', 'price': 3000, 'slug': 'goodram-8gb-3600mhz-ddr4-ram', 'resim': 'static/img/products/8gb_ram.jpg'},
    {'id': 13, 'name': 'Deneme 8GB 3600MHz DDR4 Ram', 'price': 3000, 'slug': 'goodram-8gb-3600mhz-ddr4-ram', 'resim': 'static/img/products/8gb_ram.jpg'}
]

def home(request):
    context = {'kategoriler': kategoriler,
               'slides': slides,
               'products': products
               }

    return render(request, 'index.html', context)


def category(request, slug):
    kategori = next((item for item in kategoriler if item["slug"] == slug), None)
    context = {'kategori': kategori,
               'kategoriler': kategoriler}
    return render(request, 'category.html', context)

def product(request, slug):
    item = next((i for i in products if i["slug"] == slug), None)
    context = {'products': item}
    return render(request, 'product.html', context)