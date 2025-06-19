import pytest

from products.models import Category
from products.repositories.products import (
    Product,
    ProductRepository
    )


@pytest.fixture
def product():
    return Product.objects.create(
        name="Fake Product",
        price=123,
        stock=15
    )

@pytest.mark.django_db ## Crea una db para tests
def test_get_all_when_db_empty():
    products = ProductRepository.get_all()
    assert len(products) == 0

@pytest.mark.django_db
def test_get_all_with_products():
    Product.objects.create(
        name='product_test',
        price=float(15.5),
        stock=100
    )
    Product.objects.create(
        name='product_test_1',
        price=float(15.5),
        stock=100
    )
    products = ProductRepository.get_all()
    assert len(products) == 2

@pytest.mark.django_db
def test_create():
    name = 'test_product'
    price = 152
    stock = 100
    
    product = ProductRepository.create(
        name=name,
        price=price,
        stock=stock
    )

    assert Product.objects.first() == product
    assert product.name == name

@pytest.mark.django_db
def test_create_with_category():
    category = Category.objects.create(
        name='Test Category'
    )
    name = 'test_product'
    price = 152
    stock = 100
    
    product = ProductRepository.create(
        name=name,
        price=price,
        stock=stock,
        category=category
    )

    assert Product.objects.first() == product
    assert product.name == name

@pytest.mark.django_db
def test_delete():
    product_1 = ProductRepository.create(
        name='Test 1',
        price=150,
        stock=80
    )
    product_2 = ProductRepository.create(
        name='Test 2',
        price=150,
        stock=80
    )

    ProductRepository.delete(product_2)

    products = Product.objects.all()

    assert len(products) == 1
    assert products.last() == product_1

@pytest.mark.django_db
def test_filter_by_price_range():
    product_1 = ProductRepository.create(
        name='Test 1',
        price=30,
        stock=80
    )
    product_2 = ProductRepository.create(
        name='Test 2',
        price=150,
        stock=80
    )
    product_3 = ProductRepository.create(
        name='Test 3',
        price=135,
        stock=80
    )
    product_4 = ProductRepository.create(
        name='Test 4',
        price=80,
        stock=80
    )
    min_price = 80
    max_price = 136
    products_in_range = ProductRepository.filter_by_price_range(
        min_price=min_price, max_price=max_price
    )
    
    assert len(products_in_range) == 2
    assert product_4 in products_in_range
    assert product_3 in products_in_range
    assert product_2 not in products_in_range
    assert product_1 not in products_in_range
