import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json
from server import app, db  # Ensure this import brings in your Flask app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.ServicesRequest.query')
@patch('server.db.session.commit')
def test_update_customer_service_request_success(mock_commit, mock_query, client):
    # Set up the mock service request object
    mock_service_request = MagicMock()
    mock_service_request.status = 'Pending'
    mock_query.get.return_value = mock_service_request

    # Perform the PATCH request to the endpoint with new status
    response = client.patch('/update_customer_service_requests/1', json={'status': 'Resolved'})

    # Verify the response status code and the message
    assert response.status_code == 200
    assert json.loads(response.data) == {'message': 'Service request updated successfully'}

    # Ensure that the service request status was updated and commit was called
    assert mock_service_request.status == 'Resolved'
    mock_commit.assert_called_once()

@patch('server.ServicesRequest.query')
@patch('server.db.session.commit')
def test_update_customer_service_request_not_found(mock_commit, mock_query, client):
    # Configure the mock to return None if the service request is not found
    mock_query.get.return_value = None

    # Perform the PATCH request to the endpoint
    response = client.patch('/update_customer_service_requests/999', json={'status': 'Resolved'})

    # Verify the response status code and the error message
    assert response.status_code == 404
    assert json.loads(response.data) == {'error': 'Service request not found'}

    # Check that commit was never called as there was no update
    mock_commit.assert_not_called()
