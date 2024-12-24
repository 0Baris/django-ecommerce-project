from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import RegisterUserForm, AddressForm
from django.contrib.auth.decorators import login_required
from .models import Address, Order

def login_user(request):
    if request.method == "POST":
        email = request.POST.get('loginEmail', '')
        passw = request.POST.get('loginPassword', '')
        user = authenticate(request, username=email, password=passw)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, ("Giriş Sağlanamadı, Lütfen Tekrar Deneyin."))
            return redirect('login')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('index')

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
            return redirect('index')
        else:
            messages.error(request, "Lütfen formu doğru doldurunuz.")
    else:
        form = RegisterUserForm()
    return render(request, 'register.html', {'form': form})

def terms(request):
    return render(request, 'terms.html')

@login_required
def account(request):
    return render(request, 'account.html', {'user': request.user})

@login_required
def orders(request):
    return render(request, 'orders.html', {'user': request.user})

@login_required
def adress(request):
    return render(request, 'address.html', {'user': request.user})

@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('adress')
    else:
        form = AddressForm()
    return render(request, 'address.html', {'form': form})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == "POST":
        address.delete()
        return redirect('adress')
    return render(request, 'delete_address.html', {'address': address})

@login_required
def orders_list(request, order):
    address = get_object_or_404(Order, id=address_id, user=request.user)
    if request.method == "POST":
        address.delete()
        return redirect('adress')
    return render(request, 'delete_address.html', {'address': address})