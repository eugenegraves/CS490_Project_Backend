import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json

# Import your Flask app
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.CustomersBankDetails.query')
def test_get_customer_bank_details_success(mock_query, client):
    # Mock bank details
    mock_bank_details = [
        MagicMock(
            bank_detail_id=1,
            bank_name='Bank of X',
            account_number='123456789',
            routing_number='987654321',
            customer_id=123,
            credit_score=800
        )
    ]
    mock_query.filter_by.return_value.all.return_value = mock_bank_details

    # Perform the GET request to the endpoint
    response = client.get('/get_customer_bank_details?customer_id=123')

    # Verify the response status code and data
    assert response.status_code == 200
    expected_data = [
        {
            'bank_detail_id': 1,
            'bank_name': 'Bank of X',
            'account_number': '123456789',
            'routing_number': '987654321',
            'customer_id': 123,
            'credit_score': 800
        }
    ]
    assert json.loads(response.data) == expected_data

@patch('server.CustomersBankDetails.query')
def test_get_customer_bank_details_missing_id(mock_query, client):
    # Perform the GET request without providing customer_id
    response = client.get('/get_customer_bank_details')

    # Verify the response status code and data
    assert response.status_code == 400
    assert json.loads(response.data) == {"error": "Customer ID is required."}

@patch('server.CustomersBankDetails.query')
def test_get_customer_bank_details_not_found(mock_query, client):
    # Mock empty bank details
    mock_query.filter_by.return_value.all.return_value = []

    # Perform the GET request with a non-existent customer_id
    response = client.get('/get_customer_bank_details?customer_id=999')

    # Verify the response status code and data
    assert response.status_code == 404
    assert json.loads(response.data) == {"error": "No bank details found for the specified customer."}
