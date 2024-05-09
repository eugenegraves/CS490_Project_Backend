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

@patch('server.db.session.execute')
@patch('server.db.session.commit')
def test_delete_accessory_success(mock_commit, mock_execute, client):
    # Set up the mock to simulate a successful delete operation
    mock_result = MagicMock()
    mock_result.rowcount = 1
    mock_execute.return_value = mock_result

    # Prepare the data to send with the request
    accessory_data = {'accessoryID': {'accessoire_id': '123'}}
    response = client.post('/deleteAccessoryManager', json=accessory_data)

    # Verify the response status code and data
    assert response.status_code == 200
    assert json.loads(response.data) == {'message': 'Accessory deleted successfully'}

    # Check if commit was called
    mock_commit.assert_called_once()

@patch('server.db.session.execute')
@patch('server.db.session.commit')
def test_delete_accessory_not_found(mock_commit, mock_execute, client):
    # Set up the mock to simulate no rows affected (accessory not found)
    mock_result = MagicMock()
    mock_result.rowcount = 0
    mock_execute.return_value = mock_result

    # Prepare the data to send with the request
    accessory_data = {'accessoryID': {'accessoire_id': '456'}}
    response = client.post('/deleteAccessoryManager', json=accessory_data)

    # Verify the response status code and data
    assert response.status_code == 404
    assert json.loads(response.data) == {'error': 'Accessory not found'}

@patch('server.db.session.execute')
@patch('server.db.session.commit')
def test_delete_accessory_bad_request(mock_commit, mock_execute, client):
    # Simulate sending a bad request (non-JSON)
    response = client.post('/deleteAccessoryManager', data="not-json")

    # Verify the response status code and data
    assert response.status_code == 400
    assert json.loads(response.data) == {'error': 'Request is not in JSON format'}

@patch('server.db.session.execute')
@patch('server.db.session.commit')
def test_delete_accessory_server_error(mock_commit, mock_execute, client):
    # Configure the mock to raise an exception during execute
    mock_execute.side_effect = Exception("Database failure")

    # Prepare the data to send with the request
    accessory_data = {'accessoryID': {'accessoire_id': '789'}}
    response = client.post('/deleteAccessoryManager', json=accessory_data)

    # Verify the response status code and data
    assert response.status_code == 500
    assert json.loads(response.data) == {'error': 'Database failure'}

    # Check if commit was not called due to error
    mock_commit.assert_not_called()
