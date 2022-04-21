import pytest
import json
from django.contrib.auth import get_user_model
from files.models import Folder, File
from django.core.files import File as DjangoFile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def user(db):
    return get_user_model().objects.create(
        email='virgin225@gmail.com',
        password='Azerty123$'
    )

@pytest.fixture
def other_user(db):
    return get_user_model().objects.create(
        email='laurent336@gmail.com',
        password='Azerty123$'
    )


@pytest.fixture
def auth_client(db, user):
    client = APIClient()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token.access_token))
    return client


@pytest.fixture
def root_folder(db, user):
    folder = Folder.objects.create(
        folder_name='Test Folder', 
        color='#022063',
        owner=user)
    folder.save()
    return folder


@pytest.fixture
def uploaded_file(db, root_folder, user):
    with open('README.md') as f:
        wrapped_file = DjangoFile(f)
        file = File.objects.create(
            file=wrapped_file, 
            file_name='My new file',
            owner=user,
            parent_folder=root_folder)
        file.save()
        return file
    



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


# Test retrieve a folder's details
@pytest.mark.django_db
def test_retrieve_folder_details(auth_client, root_folder):
    response = auth_client.get('/api/folders/' + str(root_folder.id))
    resp_json = json.loads(response.content)
    assert response.status_code == 200
    assert resp_json['id'] == root_folder.id


# Test rename a folder
@pytest.mark.django_db
def test_update_folder(root_folder, auth_client):
    response = auth_client.patch(f'/api/folders/{root_folder.id}', {
        'folder_name': 'New name',
    })
    resp_json = json.loads(response.content)
    assert response.status_code == 200
    assert resp_json['folder_name'] == 'New name'


# Test share a folder with another user
@pytest.mark.django_db
def test_share_folder(other_user, root_folder, auth_client):
    endpoint = f'/api/folders/{root_folder.id}/share'
    response = auth_client.post(endpoint, {
        'email': other_user.email,
    })
    resp_json = json.loads(response.content)
    assert response.status_code == 201
    assert resp_json['folder']['id'] == root_folder.id


# Test delete a folder
@pytest.mark.django_db
def test_delete_folder(root_folder, auth_client):
    endpoint = f'/api/folders/{root_folder.id}'
    response = auth_client.delete(endpoint)
    assert response.status_code == 204


# Test download a file
@pytest.mark.django_db
def test_download_file(uploaded_file, auth_client):
    endpoint = f'/api/files/{uploaded_file.id}/download'
    response = auth_client.get(endpoint, follow_redirects = True)
    assert "X-Accel-Redirect" in str(response.headers)
    assert "protected/README" in str(response.headers)

# Test delete a file
@pytest.mark.django_db
def test_delete_file(uploaded_file, auth_client):
    endpoint = f'/api/files/{uploaded_file.id}'
    response = auth_client.delete(endpoint)
    assert response.status_code == 204


# Test share a file with another user
@pytest.mark.django_db
def test_share_file(other_user, uploaded_file, auth_client):
    endpoint = f'/api/files/{uploaded_file.id}/share'
    response = auth_client.post(endpoint, {
        'email': other_user.email,
    })
    resp_json = json.loads(response.content)
    assert response.status_code == 201
    assert resp_json['file']['id'] == uploaded_file.id


# Test rename a file
@pytest.mark.django_db
def test_update_file(uploaded_file, auth_client):
    response = auth_client.patch(f'/api/files/{uploaded_file.id}', {
        'file_name': 'New file name',
    })
    resp_json = json.loads(response.content)
    assert response.status_code == 200
    assert resp_json['file_name'] == 'New file name'


# Test list user's files
@pytest.mark.django_db
def test_list_files(uploaded_file, auth_client):
    endpoint = f'/api/files/'
    response = auth_client.get(endpoint)
    resp_json = json.loads(response.content)
    assert response.status_code == 200
    assert len(resp_json) == 1
    assert resp_json[0]['id'] == uploaded_file.id


# Test Search files & folders
@pytest.mark.django_db
def test_search(auth_client, uploaded_file):
    search_keyword = 'My'
    endpoint = f'/api/search/?keyword={search_keyword}'
    response = auth_client.get(endpoint)
    resp_json = json.loads(response.content)
    assert response.status_code == 200
    assert resp_json['files'][0]['id'] == uploaded_file.id
    assert len(resp_json['files']) == 1