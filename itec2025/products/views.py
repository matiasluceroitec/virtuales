from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView, 
    ListView, 
)
from django.urls import reverse_lazy

from products.models import Product, Order
from products.forms import ProductForm, OrderForm

class ProductList(ListView):
    model = Product # Product.objects.all()
    template_name = 'products/list.html'
    context_object_name = 'products'


class ProductDetail(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id' # Nombre con el que va a encontrar el ID en la URL


class ProductDelete(DeleteView):
    model = Product
    template_name = "products/delete.html"
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('product_list') # Nombre con el que va a encontrar el ID en la URL


class ProductCreate(View):
    def get(self, request):
        return render(request, "products/create.html")

    def post(self, request):
        name = request.POST.get('name')
        stock = request.POST.get('stock')
        price = request.POST.get('price')

        Product.objects.create(
            name=name,
            stock=int(stock),
            price=float(price)
        )
        messages.success(request, 'Producto Creado')
        return render(
            request,
            'products/create.html'
        )


class ProductCreateView(CreateView):
    form_class = ProductForm
    template_name = 'products/create_from_class.html'
    success_url = reverse_lazy('product_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creador_de_productos'] = 'Creador de productos' 
        return context


class OrderList(ListView):
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'


class OrderCreate(CreateView):
    form_class = OrderForm
    template_name = 'orders/create.html'
    success_url = reverse_lazy('order_create')
