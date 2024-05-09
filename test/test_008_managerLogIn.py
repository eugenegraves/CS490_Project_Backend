import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.Managers.query')
def test_login_managers_success(mock_query, client):
    # Mock the database query result
    mock_manager = MagicMock()
    mock_manager.manager_id = 1
    mock_manager.first_name = 'John'
    mock_manager.last_name = 'Doe'
    mock_manager.email = 'johndoe@example.com'
    mock_manager.phone = '1234567890'
    mock_manager.admin_id = 1
    mock_manager.usernames = 'johndoe'
    mock_query.filter_by.return_value.first.return_value = mock_manager

    # Make a POST request to the endpoint
    response = client.post('/login_managers', json={'usernames': 'johndoe', 'password': 'password123'})

    # Verify the response
    assert response.status_code == 200
    expected_data = {
        'manager_id': 1,
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com',
        'phone': '1234567890',
        'admin_id': 1,
        'usernames': 'johndoe'
    }
    assert json.loads(response.data) == expected_data

@patch('server.Managers.query')
def test_login_managers_invalid_credentials(mock_query, client):
    # Mock the database query result to return None (indicating invalid credentials)
    mock_query.filter_by.return_value.first.return_value = None

    # Make a POST request to the endpoint with invalid credentials
    response = client.post('/login_managers', json={'usernames': 'johndoe', 'password': 'invalidpassword'})

    # Verify the response
    assert response.status_code == 401
    assert json.loads(response.data) == {'error': 'Invalid manager ID, password, or first name'}

def test_login_managers_missing_data(client):
    # Make a POST request to the endpoint without providing required data
    response = client.post('/login_managers', json={})

    # Verify the response
    assert response.status_code == 400
    assert json.loads(response.data) == {'error': 'Technician ID, password, and first name are required'}
