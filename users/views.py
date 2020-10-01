from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm

from catalog.models import Product


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            form.cleaned_data.get('username')
            messages.success(request, 'Votre compte a bien été crée')
            return redirect('catalog:index')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Les informations du profil ont été mises à jour.')
            return redirect('profile')
        else:
            return render(request, 'users/profile.html', {"Message": "Erreur, profil existant", 'u_form': u_form})
    else:
        u_form = UserUpdateForm()
    context = {'u_form': u_form}
    return render(request, 'users/profile.html', context)


@login_required
def favorite(request):
    user = request.user
    fav = Product.objects.filter(userfavorite__user_name=user.id)
    if fav:
        product = Product.objects.filter(pk__in=fav)
    else:
        product = []

    return render(request, 'users/favorite.html', {'favorite': product})
