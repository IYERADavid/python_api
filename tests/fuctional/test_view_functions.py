import os
from flask import json, request, url_for
from src.app import Family_members_info

def login_user(test_client, username, password):
    response = test_client.post(
        '/admin_login', data=dict(username=username,password=password), follow_redirects=True)
    return response

def logout_user(test_client):
    response = test_client.get('/logout', follow_redirects=True)
    return response

def test_index_page_with_fixture(test_client):
    response = test_client.get('/family-details')
    assert response.status_code == 200
    member_list = json.loads(response.data)
    family_members = Family_members_info.query.all()
    member_position = 0

    for member in family_members:
       assert member.first_name == member_list[member_position]["first_name"]
       assert member.last_name == member_list[member_position]["last_name"]
       assert member.age == member_list[member_position]["age"]
       assert member.gender == member_list[member_position]["gender"]
       assert member.phone_number == member_list[member_position]["phone_number"]
       assert member.phone_type == member_list[member_position]["phone_type"]
       member_position += 1

def test_index_page_post_with_fixture(test_client):
    response = test_client.post('/family-details')
    assert response.status_code == 405

def test_admin_login_with_fixture(test_client):
    response = test_client.get('/admin_login')
    assert response.status_code == 200
    assert request.path == url_for('admin_login')

def test_admin_login_post_with_fixture(test_client):
    def test_with_valid_credentials():
        response = login_user(
            test_client=test_client,username=os.environ.get("username"), password=os.environ.get("password"))
        assert response.status_code == 200
        assert request.path == url_for('family_member')
        logout_user(test_client)
    test_with_valid_credentials()

    def test_with_invalid_credentials():
        response = login_user(test_client=test_client,username="invalid name", password=" invalid password")
        assert response.status_code == 200
        assert request.path == url_for('admin_login')
    test_with_invalid_credentials()

def test_logout_with_fixture(test_client):
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert request.path == url_for('admin_login')

def test_logout_post_with_fixture(test_client):
    response = test_client.post('/logout')
    assert response.status_code == 405

def test_family_member_with_fixture(test_client):
    def test_getmethod_without_login():
        response = test_client.get('/new_member' , follow_redirects=True)
        assert response.status_code == 200
        assert request.path == url_for('admin_login')
    test_getmethod_without_login()

    def test_getmethod_with_login():
        login_user(
            test_client=test_client,username=os.environ.get("username"), password=os.environ.get("password"))
        response = test_client.get('/new_member')
        assert response.status_code == 200
        assert request.path == url_for('family_member')
        logout_user(test_client)
    test_getmethod_with_login()

def test_family_member_post_with_fixture(test_client):
    def test_postmethod_without_login():
        response = test_client.post('/new_member', follow_redirects=True)
        assert response.status_code == 200
        assert request.path == url_for('admin_login')
    test_postmethod_without_login()

    def test_postmethod_with_login():
        login_user(
            test_client=test_client,username=os.environ.get("username"), password=os.environ.get("password"))
        response = test_client.post('/new_member')
        assert response.status_code == 400
    test_postmethod_with_login()