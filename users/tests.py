import pytest
from django.contrib.auth import get_user_model

# Test login with wrong credentials
@pytest.mark.django_db
def test_links_list(client):
    get_user_model().objects.create_user(
        email='virgin@gmail.com', 
        password='Azerty123$'
    )

    res = client.login(email='virgin@gmail.com', password='Lolol')

    assert res is False

# test login with right credentials
@pytest.mark.django_db
def test_links_list(client):
    get_user_model().objects.create_user(
        email='virgin@gmail.com', 
        password='Azerty123$'
    )

    res = client.login(email='virgin@gmail.com', password='Azerty123$')

    assert res is True
