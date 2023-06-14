from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import generic


def index(request):
    num_product = Product.objects.all().count()
    num_instances = ProductInstance.objects.all().count()
    num_instances_available = ProductInstance.objects.filter(status__exact='i').count()
    num_manufacturer = Manufacturer.objects.count()

    return render(
        request,
        'index.html',
        context={'num_product': num_product, 'num_instances': num_instances, 'num_instances_available': num_instances_available, 'num_manufacturer': num_manufacturer},
    )


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 2


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    view_count = request.session.get('product%s_view_count' % product_id, 0)
    view_count += 1
    request.session['product%s_view_count' % product_id] = view_count
    product.view_count = view_count
    product.save()
    return render(request, 'catalog/product_detail.html', {'product': product})


class ManufacturerListView(generic.ListView):
    model = Manufacturer


class ManufacturerDetailView(generic.DetailView):
    model = Manufacturer


def search(request):
    search_input = request.GET.get('search_input')
    products = Product.objects.filter(title__icontains=search_input)
    return render(request, 'catalog/search.html', {'products': products, "search_input": search_input})


def filter_footwear(request):
    products = Product.objects.filter(type='1')
    return render(request, 'catalog/product_filter.html', {'products': products})


def filter_pants(request):
    products = Product.objects.filter(type='2')
    return render(request, 'catalog/product_filter.html', {'products': products})


def filter_outerwear(request):
    products = Product.objects.filter(type='3')
    return render(request, 'catalog/product_filter.html', {'products': products})


def account(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user)[0]
        products = cart.products.all()
        context = {'products': products}
        return render(request, 'account.html', context)
    else:
        return render(request, 'account.html')


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cart.products.add(product)
    return redirect('/products')


@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart.products.remove(product)
    return redirect('/account/welcome/')


@login_required
def buy_order(request):
    cart = Cart.objects.get(user=request.user)
    products = cart.products.all()
    for product in products:
        product.order_count += 1
        product.save()
    cart.products.clear()
    cart.save()
    return render(request, 'account.html')


def contacts(request):
    return render(request, 'contacts.html')



















