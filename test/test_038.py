import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from unittest.mock import patch
from flask import Flask
from server import app  # Import your Flask app here
from server import db, Managers

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.db.session.add')
@patch('server.db.session.commit')
@patch('server.hashlib.sha256')
def test_add_manager(mock_sha256, mock_commit, mock_add, client):
    # Mock hashlib.sha256().hexdigest() to return a consistent value
    mock_sha256.return_value.hexdigest.return_value = 'hashed_password'

    # Mock request data
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'password': 'password123',
        'username': 'johndoe'
    }

    # Perform the POST request to the endpoint
    response = client.post('/add_manager', json=data)

    # Verify the response status code and data
    assert response.status_code == 201
    assert json.loads(response.data) == {'message': 'Manager added successfully'}

    # Verify that db.session.add and db.session.commit were called with the correct arguments
    mock_add.assert_called_once()
    actual_manager = mock_add.call_args.args[0]  # Accessing the first argument directly
    assert isinstance(actual_manager, Managers)
    assert actual_manager.first_name == 'John'
    assert actual_manager.last_name == 'Doe'
    assert actual_manager.email == 'john.doe@example.com'
    assert actual_manager.phone == '1234567890'
    assert actual_manager.password == 'hashed_password'
    assert actual_manager.usernames == 'johndoe'
    mock_commit.assert_called_once()

