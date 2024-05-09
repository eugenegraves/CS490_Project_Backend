import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json
from server import app  # Ensure this import brings in your Flask app or recreate it here if needed

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.Customer.query')
def test_login_success(mock_query, client):
    # Set up mock customer data
    mock_customer = MagicMock()
    mock_customer.customer_id = 1
    mock_customer.first_name = 'John'
    mock_customer.last_name = 'Doe'
    mock_customer.email = 'johndoe@example.com'
    mock_customer.phone = '1234567890'
    mock_customer.Address = '123 Elm Street'
    mock_customer.password = 'hashed_password'
    mock_customer.usernames = 'johndoe'
    mock_customer.social_security = '123-45-6789'

    # Set up request data
    request_data = {
        'usernames': 'johndoe',
        'password': 'password123'  # Assuming this is the plain text password
    }

    # Configure mock to return the mock customer when filter_by is called
    mock_query.filter_by.return_value.first.return_value = mock_customer

    # Perform the POST request to the endpoint
    response = client.post('/login_customer', json=request_data)

    # Verify the response status code and data
    assert response.status_code == 200
    expected_data = {
        'customer_id': 1,
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com',
        'phone': '1234567890',
        'Address': '123 Elm Street',
        'password': 'hashed_password',
        'usernames': 'johndoe',
        'social_security': '123-45-6789'
    }
    assert json.loads(response.data) == expected_data

@patch('server.Customer.query')
def test_login_missing_credentials(mock_query, client):
    # Set up request data with missing credentials
    request_data = {}  # No 'usernames' and 'password' in the request data

    # Perform the POST request to the endpoint
    response = client.post('/login_customer', json=request_data)

    # Verify the response status code and data
    assert response.status_code == 400
    assert json.loads(response.data) == {'error': 'Username and password are required'}

@patch('server.Customer.query')
def test_login_invalid_credentials(mock_query, client):
    # Set up request data with invalid credentials
    request_data = {
        'usernames': 'johndoe',
        'password': 'invalid_password'
    }

    # Configure mock to return None (indicating no matching customer)
    mock_query.filter_by.return_value.first.return_value = None

    # Perform the POST request to the endpoint
    response = client.post('/login_customer', json=request_data)

    # Verify the response status code and data
    assert response.status_code == 401
    assert json.loads(response.data) == {'error': 'Invalid username or password'}
