import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from unittest.mock import patch
from flask import Flask
from server import app  # Import your Flask app here
from server import db, Customer

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.db.session.add')
@patch('server.db.session.commit')
@patch('server.hashlib.sha256')
def test_add_customer(mock_sha256, mock_commit, mock_add, client):
    # Mock hashlib.sha256().hexdigest() to return a consistent value
    mock_sha256.return_value.hexdigest.return_value = 'hashed_password'

    # Mock request data
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'Address': '123 Elm Street',
        'password': 'password123',
        'usernames': 'johndoe',
        'social_security': '123-45-6789'
    }

    # Perform the POST request to the endpoint
    response = client.post('/add_customer', json=data)

    # Verify the response status code and data
    assert response.status_code == 201
    assert json.loads(response.data) == {'message': 'Customer added successfully'}

    # Verify that db.session.add and db.session.commit were called with the correct arguments
    mock_add.assert_called_once()
    actual_customer = mock_add.call_args.args[0]  # Accessing the first argument directly
    assert isinstance(actual_customer, Customer)
    assert actual_customer.first_name == 'John'
    assert actual_customer.last_name == 'Doe'
    assert actual_customer.email == 'john.doe@example.com'
    assert actual_customer.phone == '1234567890'
    assert actual_customer.Address == '123 Elm Street'
    assert actual_customer.password == 'hashed_password'
    assert actual_customer.usernames == 'johndoe'
    assert actual_customer.social_security == '123-45-6789'
    mock_commit.assert_called_once()
