from products.models import Product


class ProductRepository:
    """
    Clase de repositorio que se encargara de conectarse con la db
    para manipular productos
    """
    @staticmethod
    def create(
        name: str, 
        price: float, 
        stock: int,
    ) -> Product:
        return Product.objects.create(
            name=name,
            price=price,
            stock=stock,
        )

    @staticmethod
    def delete(product: Product) -> bool:
        try:
            Product.delete()
        except Product.DoesNotExist:
            raise ValueError("El producto no existe")
        
    @staticmethod
    def update(product: Product, price: float, stock: int) -> Product:
        product.price = price
        product.stock = stock
        product.save()

        return product

    @staticmethod
    def get_all() -> list[Product]:
        """
        Obtiene todos los objects (Product)
        """
        return Product.objects.all()

    @staticmethod
    def get_by_id(product_id: int) -> Product:
        """
        Obtiene un producto a partir de su id
        """
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None
    
    @staticmethod
    def search_by_name(name: str) -> list[Product]:
        """
        Buscar los products que contengan el nombre ingresado
        """
        return Product.objects.filter(name__icontains=name)
        #################(atributo__que-contenga__cadena-que-le-paso)

    @staticmethod
    def filter_by_price_range(
        min_price: float, max_price: float
    ) -> list[Product]:
        """ 
        Retorna un listado de productos cuyo precio esta en el rango establecido
        """
        return Product.objects.filter(price__range=(min_price, max_price))
        # Podemos utilizar cualquiera de los dos (range incluye los extremos al igual que gte y lte)
        return Product.objects.filter(
            price__gte=min_price, 
            price__lte=max_price
        )