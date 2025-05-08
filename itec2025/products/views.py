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
    model = Product
    template_name = 'products/create_from_class.html'
    success_url = reverse_lazy('product_list')
    fields = ['name', 'price', 'stock']

    def form_valid(self, form):
        messages.success(self.request, "Producto Creado")
        return super().form_valid(form)


class OrderList(ListView):
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'
