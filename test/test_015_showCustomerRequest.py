import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from flask import Flask, json
from server import app  # Ensure the server and db are appropriately imported

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.db.session.query')
def test_show_customer_service_requests(mock_query, client):
    # Create a proper datetime object for testing
    proposed_datetime = datetime(2023, 4, 1, 10, 0)

    # Mock the query return value
    mock_service_requests = [
        (MagicMock(service_request_id=1), "Oil Change", 29.99, "Standard Oil Change",
         proposed_datetime, "pending", 123, 2, 101, "JohnDoe", "555-0123")
    ]

    mock_query.return_value.join.return_value.join.return_value.filter.return_value.all.return_value = mock_service_requests

    # Perform the GET request to the endpoint
    response = client.get('/show_customer_service_requests/')

    # Verify the response status code and data
    assert response.status_code == 200
    expected_data = [{
        'service_request_id': 1,
        'service_name': "Oil Change",
        'service_price': 29.99,
        'description': "Standard Oil Change",
        'proposed_datetime': "2023-04-01T10:00:00",
        'status': "pending",
        'car_id': 123,
        'service_offered_id': 2,
        'customer_id': 101,
        'customer_username': "JohnDoe",
        'customer_phone': "555-0123"
    }]
    # Using response.get_json() to ensure format and type alignment in comparison
    assert response.get_json() == expected_data
