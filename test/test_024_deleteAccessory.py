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

@patch('server.db.session.commit')
@patch('server.db.session.execute')
def test_delete_accessory_success(mock_execute, mock_commit, client):
    """Test successful deletion of an accessory."""
    # Setup the mock to simulate database execute and row count
    mock_result = MagicMock()
    mock_result.rowcount = 1  # Simulate one row affected (deletion successful)
    mock_execute.return_value = mock_result

    # Prepare the mock JSON data
    data = {'accessoryID': {'accessoire_id': '1'}}

    # Perform the POST request to the endpoint
    response = client.post('/deleteAccessoryManager', json=data)

    # Verify the response status code and data
    assert response.status_code == 200
    assert json.loads(response.data) == {'message': 'Accessory deleted successfully'}

    # Verify commit was called
    mock_commit.assert_called_once()

@patch('server.db.session.execute')
def test_delete_accessory_not_found(mock_execute, client):
    """Test deletion attempt for a non-existent accessory."""
    # Setup the mock to simulate no rows affected
    mock_result = MagicMock()
    mock_result.rowcount = 0  # Simulate no rows affected (no deletion occurred)
    mock_execute.return_value = mock_result

    # Prepare the mock JSON data
    data = {'accessoryID': {'accessoire_id': '999'}}

    # Perform the POST request to the endpoint
    response = client.post('/deleteAccessoryManager', json=data)

    # Verify the response status code and data
    assert response.status_code == 404
    assert json.loads(response.data) == {'error': 'Accessory not found'}

@patch('server.db.session.execute')
def test_delete_accessory_invalid_request(mock_execute, client):
    """Test deletion attempt with an invalid request format."""
    # Perform the POST request to the endpoint without JSON data
    response = client.post('/deleteAccessoryManager', data="Not JSON")

    # Verify the response status code and data
    assert response.status_code == 400
    assert json.loads(response.data) == {'error': 'Request is not in JSON format'}
