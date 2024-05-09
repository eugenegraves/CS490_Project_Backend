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

@patch('server.Technicians.query')
def test_login_technicians_valid_credentials(mock_query, client):
    # Mocking the response from the database query
    mock_technician = MagicMock()
    mock_technician.technicians_id = 1
    mock_technician.first_name = 'John'
    mock_technician.last_name = 'Doe'
    mock_technician.email = 'john.doe@example.com'
    mock_technician.phone = '1234567890'
    mock_technician.manager_id = 123
    mock_technician.usernames = 'johndoe'
    
    mock_query.filter_by.return_value.first.return_value = mock_technician

    # Sending a POST request to the endpoint with valid credentials
    response = client.post('/login_technicians', json={'usernames': 'johndoe', 'password': 'password123'})

    assert response.status_code == 200
    expected_data = {
        'technicians_id': 1,
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'manager_id': 123,
        'usernames': 'johndoe'
    }
    assert json.loads(response.data) == expected_data

@patch('server.Technicians.query')
def test_login_technicians_invalid_credentials(mock_query, client):
    # Mocking the response from the database query to return None (no technician found)
    mock_query.filter_by.return_value.first.return_value = None

    # Sending a POST request to the endpoint with invalid credentials
    response = client.post('/login_technicians', json={'usernames': 'invaliduser', 'password': 'invalidpassword'})

    assert response.status_code == 401
    assert json.loads(response.data) == {'error': 'Invalid technician ID, password, or first name'}

def test_login_technicians_missing_credentials(client):
    # Sending a POST request to the endpoint with missing credentials
    response = client.post('/login_technicians', json={})

    assert response.status_code == 400
    assert json.loads(response.data) == {'error': 'Technician ID, password, and first name are required'}
