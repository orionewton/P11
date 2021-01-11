import json

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.views.generic import DetailView

from .models import Product, UserFavorite


# Create your views here.


def index(request):
    return render(request, 'catalog/index.html')


def legal(request):
    return render(request, 'catalog/mlegal.html')


def autocomplete(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        products = Product.objects.filter(
            name__icontains=query).order_by("-nutrition_grade")[:10]
        results = []
        for p in products:
            product_dict = p.name
            results.append(product_dict)
        data = json.dumps(results)
    else:
        data = 'fail'
    return HttpResponse(data, 'application/json')


def search(request):
    query = request.GET.get('query')

    try:
        product = Product.objects.filter(name=query).first()
        substitutes = Product.objects.filter(
            category=product.category,
            nutrition_grade__lt=product.nutrition_grade).order_by(
            "nutrition_grade")

        paginator = Paginator(substitutes, 6)
        page = request.GET.get('page')
        alt_products = paginator.get_page(page)

        context = {
            'alt_products': alt_products,
            'paginate': True,
            'title': query,
            'image': product.picture,
        }

    except AttributeError:
        messages.warning(request, "Ce produit n'existe pas. "
                                  "Vérifiez l'orthographe de la recherche")
        return redirect('catalog:index')

    return render(request, 'catalog/search.html', context)


class ProductDetail(DetailView):
    model = Product
    template = 'catalog/product_detail.html'


@login_required
def add_favorite(request, product_id):
    try:
        UserFavorite.objects.get(
            user_name_id=request.user.id, product_id=product_id)
        messages.warning(request, 'Ce produit est déjà dans vos favoris.')
        return redirect(request.META.get('HTTP_REFERER'))
    except ObjectDoesNotExist:
        UserFavorite.objects.create(
            user_name_id=request.user.id, product_id=product_id)
        messages.success(request, 'Le produit a bien été enregistré.')
        return redirect(request.META.get('HTTP_REFERER'))
