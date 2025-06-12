from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps

from products.models import OrderDetail, OrderDetailAuditLog


@receiver(post_save, sender='products.OrderDetail')
def update_stock_on_order_create(sender, instance, created, **kwargs):
    """
    Signal que se activa cuando se crea un nuevo detalle de pedido
    
    Args: 
    - sender: El modelo que disparo el singal (OrderDetail)
    - instace: La instancia del modelo que creo
    - created: booleano si se creo la instancia es True si no es False
    """

    if created:
        # Product = apps.get_model('products', 'Product') Vea el video del 11-6 para enteder que hace
        product = instance.product
        product.stock -= instance.quantity
        product.save()
    

@receiver(post_delete, sender=OrderDetail)
def update_stock_on_order_delete(sender, instance, **kwargs):
    product = instance.product
    product.stock += instance.quantity
    product.save()

@receiver(post_save, sender=OrderDetail)
def create_audit_log_order_detail(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    OrderDetailAuditLog.objects.create(
        order_detail=instance,
        action=action,
        quantity=instance.quantity,
        product_name=instance.product.name
    )