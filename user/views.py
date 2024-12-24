from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import RegisterUserForm

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
