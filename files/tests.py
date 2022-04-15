import pytest
import json
from django.contrib.auth import get_user_model
from files.models import Folder, File
from rest_framework.test import APIClient



@pytest.fixture
def auth_client(db):
    client = APIClient()
    usr = client.post(
        '/signup',
        {'email': 'virgin225@gmail.com',
        'password': 'Azerty123$',
        'first_name': 'Virgin',
        'last_name': 'Bitton'},
    )
    login = client.post(
        '/api/token/',
        {'email': 'virgin225@gmail.com',
        'password': 'Azerty123$'},
    )
    resp_json = json.loads(login.content)
    print(resp_json)
    access_token = resp_json['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    return client

@pytest.fixture
def user(db):
    return get_user_model().objects.create(
        email='virgin225@gmail.com',
        password='Azerty123$'
    )

@pytest.fixture
def root_folder(db, user):
    return Folder.objects.create(
        folder_name='Test Folder', 
        color='#022063',
        owner=user)



# Test retrieve users's folders list
@pytest.mark.django_db
def test_retrieve_my_folders(auth_client):
    response = auth_client.get('/api/folders/')
    resp_json = json.loads(response.content)
    assert response.status_code == 200
    assert len(resp_json) >= 1


# Test create a folder
@pytest.mark.django_db
def test_create_folder(root_folder, auth_client):
    response = auth_client.post('/api/folders/', {
        'folder_name': 'My Test Folder',
        'parent_folder': root_folder.id,
        'color': '#022063'
    })
    resp_json = json.loads(response.content)

    assert response.status_code == 201
    assert resp_json['id']

# Test update a folder
@pytest.mark.django_db
def test_update_folder(root_folder, auth_client):
    response = auth_client.patch(f'/api/folders/{root_folder.id}', {
        'folder_name': 'New name',
    })
    resp_json = json.loads(response.content)
    assert response.status_code == 200
    assert resp_json['folder_name'] == 'New name'
