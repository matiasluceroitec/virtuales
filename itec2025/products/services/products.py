from decimal import Decimal
from typing import List

from products.models import Product
from products.repositories.products import ProductRepository

class ProductService:
    """
    Se puede utilizar con el init, y necesitan pasar siempre self
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def get_all(self) -> list[Product]:
        return self.product_repository.get_all()
    """
    
    @staticmethod
    def get_all() -> list[Product]:
        return ProductRepository.get_all() 
    
    @staticmethod
    def delete(product_id: int) -> bool:
        product = ProductRepository.get_by_id(product_id=product_id)
        if product:
            return ProductRepository.delete(product=product)
        return False
    
    @staticmethod
    def update(
        product_id: int,
        price: float,
        stock: int,
    ) -> bool:
        product = ProductRepository.get_by_id(product_id=product_id)
        if product:
            ProductRepository.update(
                product=product,
                price=price,
                stock=stock,
            )
        
    @staticmethod
    def sum_total_price(product_list: List[Product]) -> Decimal:
        total = Decimal(0)
        for product in product_list:
            total +=( product.price * product.stock)
        return total
