import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json

# Import your Flask app instance
from server import app  # Update this import with your actual Flask app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


@patch('server.Admin.query')
def test_login_admin_successful(mock_query, client):
    # Mock data
    mock_admin = MagicMock()
    mock_admin.admin_id = 1
    mock_admin.first_name = 'John'
    mock_admin.last_name = 'Doe'
    mock_admin.usernames = 'john_doe'
    mock_admin.phone = '123-456-7890'

    # Configure the mock to return the mock admin when filter_by().first() is called
    mock_query.filter_by.return_value.first.return_value = mock_admin

    # Make a request to the endpoint
    response = client.post('/login_admin', json={'usernames': 'john_doe', 'password': 'test123'})

    # Assert the response
    assert response.status_code == 200
    expected_data = {
        'admin_id': 1,
        'first_name': 'John',
        'last_name': 'Doe',
        'usernames': 'john_doe',
        'phone': '123-456-7890'
    }
    assert json.loads(response.data) == expected_data

@patch('server.Admin.query')
def test_login_admin_invalid_credentials(mock_query, client):
    # Configure the mock to return None when filter_by().first() is called
    mock_query.filter_by.return_value.first.return_value = None

    # Make a request to the endpoint with invalid credentials
    response = client.post('/login_admin', json={'usernames': 'invalid_user', 'password': 'invalid_password'})

    # Assert the response
    assert response.status_code == 401
    assert json.loads(response.data) == {'error': 'Invalid admin ID, password, or first name'}

def test_login_admin_missing_fields(client):
    # Make a request to the endpoint with missing fields
    response = client.post('/login_admin', json={})

    # Assert the response
    assert response.status_code == 400
    assert json.loads(response.data) == {'error': 'Technician ID, password, and first name are required'}
