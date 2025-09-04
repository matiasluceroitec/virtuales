import pytest

from django.contrib.auth.models import User
from django.urls import reverse

from products.models import Customer


@pytest.mark.django_db
def test_get_all_users(api_client):
    user_1 = User.objects.create(
        username="user1", 
        email="u1@tests.com"
    )
    user_2 = User.objects.create(
        username="user2", 
        email="u2@tests.com", 
        is_active=False
    )
    url = reverse('users-list')
    response = api_client.get(url)
    body = response.json()

    assert response.status_code == 200
    assert body == [
        {
            "email": user_1.email,
            "pk": user_1.pk,
            "first_name": '',
            "username":user_1.username,
            "last_name": '',
            "is_active": True            
        },
        {
            "email": user_2.email,
            "pk": user_2.pk,
            "first_name": '',
            "username":user_2.username,
            "last_name": '',
            "is_active": False            
        }
    ]

@pytest.mark.django_db
def test_get_all_users_empty_users(api_client):
    url = reverse('users-list')
    response = api_client.get(url)
    body = response.json()

    assert response.status_code == 200
    assert body == []

@pytest.mark.django_db
def test_get_all_users_with_11_user(api_client):
    for x in range(11):
        User.objects.create(
            username=f"user{x}", 
            email=f"u{x}@tests.com"
        )
    url = reverse('users-list')
    response = api_client.get(url)
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 11

@pytest.mark.django_db
def test_user_create(api_client):
    """
    Testea la creacion de un usuario llamando a /api/users/ [POST]
    payload = {
        "username": "",
        "email": "",
        "first_name": "",
        "last_name": "",
        "is_active": false,
        "password": ""
    }
    """
    users = User.objects.all()
    assert users.count() == 0

    payload = {
        "username": "test_user",
        "email": "test_user@test.com",
        "first_name": "Test Name",
        "last_name": "Test Lastname",
        "is_active": True,
        "password": "fake123"
    }
    url = reverse('users-list')
    response = api_client.post(path=url, data=payload, format='json')
    
    body = response.json()
    users = User.objects.all()
    user = users.first()
    assert response.status_code == 201
    assert "password" not in body
    assert body['username'] == 'test_user'
    assert body['last_name'] == 'Test Lastname'
    assert body['first_name'] == 'Test Name'
    assert body['email'] == 'test_user@test.com'
    assert body['is_active']
    assert users.count() == 1
    assert user.email == 'test_user@test.com'
    assert Customer.objects.all().count() == 1
    assert Customer.objects.filter(name=user.first_name).exists()

    assert user.check_password('fake123')

@pytest.mark.django_db
def test_user_with_invalid_username(api_client):
    """
    Testea la creacion de un usuario llamando a /api/users/ [POST] con nombre de usuario invalido
    payload = {
        "username": "",
        "email": "",
        "first_name": "",
        "last_name": "",
        "is_active": false,
        "password": ""
    }
    """
    users = User.objects.all()
    assert users.count() == 0

    payload = {
        "username": "$$$$$",
        "email": "test_user@test.com",
        "first_name": "Test Name",
        "last_name": "Test Lastname",
        "is_active": True,
        "password": "fake123"
    }
    url = reverse('users-list')
    response = api_client.post(path=url, data=payload, format='json')
    
    body = response.json()
    users = User.objects.all()
    assert users.count() == 0
    assert response.status_code == 400
    assert body["username"] == ["Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."]

@pytest.mark.django_db
def test_user_with_invalid_password(api_client):
    """
    Testea la creacion de un usuario llamando a /api/users/ [POST] sin password
    """
    users = User.objects.all()
    assert users.count() == 0

    payload = {
        "username": "test_user",
        "email": "test_user@test.com",
        "first_name": "Test Name",
        "last_name": "Test Lastname",
        "is_active": True,
        "password": ""
    }
    url = reverse('users-list')
    response = api_client.post(path=url, data=payload, format='json')
    
    body = response.json()
    users = User.objects.all()
    assert users.count() == 0
    assert response.status_code == 400
    assert body["password"] == ["This field may not be blank."]

@pytest.mark.django_db
def test_user_retrieve(api_client):
    """
    GET /api/users/<pk> debe devolver los campos del usuario
    """
    user_1 = User.objects.create(
        username="user1", 
        email="u1@tests.com"
    )
    user_2 = User.objects.create(
        username="user2", 
        email="u2@tests.com", 
        is_active=False
    )

    url = reverse("users-detail", args=[user_2.pk])
    print(url)
    response = api_client.get(url)

    status = response.status_code
    data = response.json()

    assert status == 200
    assert data['username'] == user_2.username
    assert data['email'] == user_2.email

@pytest.mark.django_db
def test_user_retrieve_user_no_found(api_client):
    """
    GET /api/users/<pk> debe devolver los campos del usuario
    """
    url = reverse("users-detail", args=["3"])
    response = api_client.get(url)

    status = response.status_code
    data = response.json()

    assert status == 404
    assert data['detail'] == "No User matches the given query."

@pytest.mark.django_db
def test_update_put_user(api_client):
    """
    PUT /api/users/<pk>
    actualiza los campos del usuario, enviando siempre toda la informacion requerida
    """
    user = User.objects.create(
        username="user1", 
        email="u1@tests.com",
        first_name="Nombre viejo",
        last_name="Apellido viejo"
    )
    payload = {
        "first_name" : "Nombre Nuevo",
        "username":"user1", 
        "email":"u1@tests.com",
        "last_name":"Apellido viejo"
    }

    url = reverse("users-detail", args=[user.pk])
    response = api_client.put(url, payload, format='json')
    
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.first_name == "Nombre Nuevo"
    assert user.last_name == "Apellido viejo"

@pytest.mark.django_db
def test_update_patch_user(api_client):
    """
        PATCH /api/users/<pk>
        actualiza el/los campos del usuario, enviando solo la informacion a modificar
    """
    user = User.objects.create(
        username="user1", 
        email="u1@tests.com",
        first_name="Nombre viejo",
        last_name="Apellido viejo"
    )
    payload = {
        "first_name" : "Nombre Nuevo",
    }

    url = reverse("users-detail", args=[user.pk])
    response = api_client.patch(url, payload, format='json')
    
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.first_name == "Nombre Nuevo"
    assert user.last_name == "Apellido viejo"
    ...

@pytest.mark.django_db
def test_soft_delete_user(api_client):
    """
    DELETE /api/users/<pk>
    Debe desactivar el usuario, y devolver 200 y un mensaje
    
    """
    user = User.objects.create(
        username="user1", 
        email="u1@tests.com",
        first_name="Nombre viejo",
        last_name="Apellido viejo",
        is_active=True
    )
    url = reverse("users-detail", args=[user.pk])
    response = api_client.delete(url)

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.is_active is False
    assert response.json()['detail'] == f"User {user.username} deactivated"

@pytest.mark.django_db
def test_soft_delete_user_call_two_times(api_client):
    """
    DELETE /api/users/<pk>
    Debe desactivar el usuario, y devolver 200 y un mensaje
    
    """
    user = User.objects.create(
        username="user1", 
        email="u1@tests.com",
        first_name="Nombre viejo",
        last_name="Apellido viejo",
        is_active=True
    )
    url = reverse("users-detail", args=[user.pk])
    response = api_client.delete(url)

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.is_active is False
    assert response.json()['detail'] == f"User {user.username} deactivated"

    url = reverse("users-detail", args=[user.pk])
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.is_active is False
    assert response.json()['detail'] == f"User {user.username} deactivated"
