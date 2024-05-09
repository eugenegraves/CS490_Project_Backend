import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.db.session.query')
def test_show_assigned_services_success(mock_query, client):
    mock_query_instance = mock_query.return_value
    mock_join_instance = mock_query_instance.join.return_value
    mock_filter_instance = mock_join_instance.filter.return_value
    mock_options_instance = mock_filter_instance.options.return_value

    mock_result = MagicMock()
    mock_result.assigned_service_id = 101
    mock_result.technician.first_name = 'John'
    mock_result.technician.last_name = 'Doe'
    mock_result.technician.email = 'john.doe@example.com'
    mock_result.technician.phone = '555-1234'
    mock_service_request = MagicMock()
    mock_service_request.proposed_datetime = None
    mock_service_request.status = 'Pending'
    mock_service_request.car_id = 202
    mock_service_request.service_offered_id = 303
    mock_customer = MagicMock()
    mock_customer.first_name = 'Alice'
    mock_customer.last_name = 'Smith'
    mock_customer.phone = '555-6789'
    mock_service = MagicMock()
    mock_service.name = 'Oil Change'
    mock_service.price = 29.99
    mock_service.description = 'Standard oil change'

    mock_row = (
        mock_result,
        mock_service_request,
        1,  # service_request_id
        mock_customer.first_name,
        mock_customer.last_name,
        mock_customer.phone,
        mock_service.name,
        mock_service.price,
        mock_service.description,
    )

    mock_options_instance.all.return_value = [mock_row]

    response = client.get('/show_assigned_services/123')
    expected_data = [{
        'assigned_service_id': 101,
        'service_request_id': 101,
        'technician_first_name': 'John',
        'technician_last_name': 'Doe',
        'technician_email': 'john.doe@example.com',
        'technician_phone': '555-1234',
        'service_name': 'Oil Change',
        'service_price': 29.99,
        'service_description': 'Standard oil change',
        'proposed_datetime': None,
        'status': 'Pending',
        'car_id': 202,
        'service_offered_id': 303,
        'customer_first_name': 'Alice',
        'customer_last_name': 'Smith',
        'customer_phone': '555-6789'
    }]
    assert response.get_json() == expected_data
