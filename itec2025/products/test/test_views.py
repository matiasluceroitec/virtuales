import pytest

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from products.models import Product

@pytest.fixture
def product():
    return Product.objects.create(
        name="Fake Product",
        price=123,
        stock=15
    )

@pytest.fixture
def client():
    """ Client de prueba para llamadas """
    return Client()

@pytest.fixture
def admin_client():
    client = Client()
    admin_user = User.objects.create_superuser(
        username='admin',
        email='user@admin.com',
        password='123211122541'
    )
    client.force_login(admin_user)
    return client


@pytest.mark.django_db
def test_product_list_view(client, product):
    url = reverse('product_list')

    response = client.get(url)
    
    #import ipdb; ipdb.set_trace()
    assert response.status_code == 200
    assert product in response.context['products']
    assert 'products/list.html' in [template.name for template in response.templates]
    assert b'Fake Product' in response.content
