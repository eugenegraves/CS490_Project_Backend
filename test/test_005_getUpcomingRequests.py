import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json
from server import app
import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.db.session.query')
def test_get_upcoming_week_requests(mock_query, client):
    # Define mock data for the service requests
    mock_service_request_1 = MagicMock()
    mock_service_request_1.service_request_id = 1
    mock_service_request_1.proposed_datetime = datetime.datetime(2024, 5, 10, 10, 0, 0)  # Corrected datetime format
    mock_service_request_1.status = 'accepted'
    mock_service_request_1.service_name = 'Oil Change'
    mock_service_request_1.first_name = 'John'
    mock_service_request_1.last_name = 'Doe'
    mock_service_request_1.make = 'Toyota'
    mock_service_request_1.model = 'Camry'
    mock_service_request_1.year = 2020

    mock_service_request_2 = MagicMock()
    mock_service_request_2.service_request_id = 2
    mock_service_request_2.proposed_datetime = datetime.datetime(2024, 5, 11, 14, 0, 0)  # Corrected datetime format
    mock_service_request_2.status = 'assigned'
    mock_service_request_2.service_name = 'Brake Repair'
    mock_service_request_2.first_name = 'Alice'
    mock_service_request_2.last_name = 'Smith'
    mock_service_request_2.make = 'Honda'
    mock_service_request_2.model = 'Accord'
    mock_service_request_2.year = 2018

    # Set up the mock to return the mock service requests
    mock_query.return_value.join.return_value.outerjoin.return_value.outerjoin.return_value.join.return_value.filter.return_value.all.return_value = [mock_service_request_1, mock_service_request_2]

    # Perform the GET request to the endpoint
    response = client.get('/get_upcoming_week_requests')

    # Verify the response status code and data
    assert response.status_code == 200
    expected_data = {
        'accepted_service_requests': [
            {
                'service_request_id': 1,
                'date': '2024-05-10',
                'date_time': '2024-05-10 10:00',
                'service_name': 'Oil Change',
                'technician_name': 'John Doe',
                'car_info': {
                    'make': 'Toyota',
                    'model': 'Camry',
                    'year': 2020
                },
                'status': 'accepted'
            }
        ],
        'assigned_service_requests': [
            {
                'service_request_id': 2,
                'date': '2024-05-11',
                'date_time': '2024-05-11 14:00',
                'service_name': 'Brake Repair',
                'technician_name': 'Alice Smith',
                'car_info': {
                    'make': 'Honda',
                    'model': 'Accord',
                    'year': 2018
                },
                'status': 'assigned'
            }
        ]
    }
    assert json.loads(response.data) == expected_data

