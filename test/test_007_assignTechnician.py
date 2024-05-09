import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# your_test_file.py

import pytest
import datetime
from unittest.mock import patch, MagicMock
from flask import json
from server import app  # Import your Flask app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.ServicesRequest.query')
@patch('server.AssignedServices.query')
def test_assign_technicians(mock_assigned_services_query, mock_services_request_query, client):
    # Mock data
    mock_service_request = MagicMock()
    mock_service_request.proposed_datetime = datetime.datetime(2024, 5, 9, 12, 0)  # Assuming a specific datetime
    mock_service_request.status = 'proposed'  # Assuming initial status is 'proposed'

    mock_assigned_services_query.filter.return_value.first.return_value = None  # Assuming no conflicts
    mock_services_request_query.filter_by.return_value.first.return_value = mock_service_request  # Assuming service request found

    # POST request data
    data = {
        'technician_id': 1,
        'service_request_id': 1
    }

    response = client.post('/assign_technicians', json=data)

    assert response.status_code == 200
    assert json.loads(response.data) == {'message': 'Technician assigned successfully'}


