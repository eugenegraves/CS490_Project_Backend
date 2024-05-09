import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from unittest.mock import patch, MagicMock
from flask import Flask
from server import app  # Import your Flask app here

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.db.session.add')
@patch('server.db.session.commit')
@patch('server.hashlib.sha256')
def test_add_technician(mock_sha256, mock_commit, mock_add, client):
    # Mock hashlib.sha256().hexdigest() to return a consistent value
    mock_sha256.return_value.hexdigest.return_value = 'hashed_password'

    # Mock request data
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@example.com',
        'username': 'johndoe',
        'phone': '1234567890',
        'password': 'password123',
        'manager_id': 1
    }

    # Perform the POST request to the endpoint
    response = client.post('/add_technician', json=data)

    # Verify the response status code and data
    assert response.status_code == 201
    assert json.loads(response.data) == {'message': 'Technician added successfully'}

    # Verify that db.session.add and db.session.commit were called with the correct arguments
    mock_add.assert_called_once()
    actual_technician = mock_add.call_args.args[0]  # Accessing the single argument directly
    assert actual_technician.first_name == 'John'
    assert actual_technician.last_name == 'Doe'
    assert actual_technician.email == 'john.doe@example.com'
    assert actual_technician.usernames == 'johndoe'
    assert actual_technician.phone == '1234567890'
    assert actual_technician.password == 'hashed_password'
    assert actual_technician.manager_id == 1
    mock_commit.assert_called_once()
