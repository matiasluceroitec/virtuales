import pytest

from products.forms import ProductForm


@pytest.mark.django_db
def test_product_form_is_valid():
    form_data = {
        'name': 'Product Test',
        'price': '99.8',
        'stock': '15'
    }

    form = ProductForm(data=form_data)

    assert form.is_valid()

@pytest.mark.parametrize(
        'name, price, stock, expected_errors', [
        ('', '88.8', '10', ['name']),
        ('Test 2', '5', 'abcd', ['stock'])
    ]
)
@pytest.mark.django_db
def test_product_form_is_valid_parametrized(name, price, stock, expected_errors):
    form_data = {
        'name':name,
        'price': price,
        'stock': stock,
    }
    
    form = ProductForm(data=form_data)
    
    assert not form.is_valid()
    assert set(expected_errors) == set(form.errors.keys())
    
