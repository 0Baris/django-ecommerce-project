from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import RegisterUserForm, AddressForm
from django.contrib.auth.decorators import login_required
from .models import Address
from order.models import Order
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

# Kullanıcı giriş fonksiyonu
def login_user(request):
    if request.method == "POST":
        email = request.POST.get('loginEmail', '')
        passw = request.POST.get('loginPassword', '')
        user = authenticate(request, username=email, password=passw)
        if user is not None:
            login(request, user)
            return redirect('catalog:index')
        else:
            messages.success(request, ("Giriş Sağlanamadı, Lütfen Tekrar Deneyin."))
            return redirect('user:login')
    return render(request, 'login.html')

# Kullanıcı çıkış fonksiyonu
def logout_user(request):
    logout(request)
    return redirect('catalog:index')

# Kullanıcı kayıt fonksiyonu
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                messages.error(request, "Bu email zaten kayıtlı!")
                return redirect('register')
            user = form.save(commit=False)
            user.username = email
            user.save()
            backend = 'user.backends.EmailBackend'
            login(request, user, backend=backend)
            messages.success(request, "Kayıt başarılı!")
            return redirect('catalog:index')
        else:
            messages.error(request, "Lütfen formu doğru doldurunuz.")
    else:
        form = RegisterUserForm()
    return render(request, 'register.html', {'form': form})

# Kullanıcı hesap sayfası fonksiyonu
@login_required
def account(request):
    return render(request, 'account.html', {'user': request.user})

# Kullanıcı siparişleri fonksiyonu
@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-order_date')
    if not user_orders.exists():
        messages.info(request, "Henüz siparişiniz bulunmamaktadır.")
    return render(request, 'orders.html', {'user': request.user, 'orders': user_orders})

# Kullanıcı adres sayfası fonksiyonu
@login_required
def adress(request):
    return render(request, 'address.html', {'user': request.user})

# Kullanıcı adres ekleme fonksiyonu
@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.city = request.POST.get('city')
            address.district = request.POST.get('district')
            address.save()
            return redirect('user:adress')
    else:
        form = AddressForm()
    return render(request, 'address.html', {'form': form})

# Kullanıcı adres silme fonksiyonu
@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == "POST":
        address.delete()
        return redirect('user:adress')
    return render(request, 'delete_address.html', {'address': address})

def forgot_password(request):
    User = get_user_model()

    if request.method == "POST":
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            send_mail(
                'Şifre yenileme isteği.',
                message,
                'gamingissiz@gmail.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, "Şifre sıfırlama bağlantısı email adresinize gönderildi.")
        else:
            messages.error(request, "Bu email adresi ile kayıtlı bir kullanıcı bulunamadı.")
        return redirect('catalog:index')
    return render(request, 'forgot_password.html')