import pytest
import json
from django.contrib.auth import get_user_model

# Test account creation
@pytest.mark.django_db
def test_create_account_route(client):
    response = client.post(
            '/signup',
            {'email': 'virgin223@gmail.com',
            'password': 'Azerty123$',
            'first_name': 'Paul',
            'last_name': 'Larousse'},
    )
    resp_json = json.loads(response.content)

    assert response.status_code == 200
    assert resp_json['email'] == 'virgin223@gmail.com'


# Test login
@pytest.mark.django_db
def test_login_route(client):
    #Create account
    client.post(
            '/signup',
            {'email': 'virgin223@gmail.com',
            'password': 'Azerty123$',
            'first_name': 'Paul',
            'last_name': 'Larousse'}
    )
    #Login with previously created acccount
    response = client.post(
            '/api/token/',
            {'email': 'virgin223@gmail.com',
            'password': 'Azerty123$'},
        )
    resp_json = json.loads(response.content)
    print(resp_json)
    assert response.status_code == 200
    assert len(resp_json['access']) >= 2