from django.db import models
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_("Product name"), max_length=255)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} for {self.customer.name}"


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='details',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField()
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id)


class OrderDetailAuditLog(models.Model):
    """
    Modelo para registrar los cambios en OrderDetail
    """
    order_detail = models.ForeignKey(
        OrderDetail,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    action = models.CharField(
        max_length=12,
        choices=[
            ('created', _('Created')),
            ('updated', _('Updated'))
        ],
    )
    quantity = models.IntegerField()
    product_name = models.CharField(
        max_length=255,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )
