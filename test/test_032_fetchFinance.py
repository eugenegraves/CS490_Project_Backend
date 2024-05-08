import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json, jsonify
from server import app  # Make sure to import your Flask app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.FinanceContract.query')
def test_fetch_finance_success(mock_query, client):
    # Create mock finance items
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.customer_id = 123
    mock_item.first_name = 'John'
    mock_item.last_name = 'Doe'
    mock_item.car_year = 2020
    mock_item.car_make = 'Toyota'
    mock_item.car_model = 'Camry'
    mock_item.car_price = 30000.00
    mock_item.credit_score = 720
    mock_item.finance_decision = 'Approved'
    mock_item.loan_term = 60
    mock_item.loan_apr = 3.5
    mock_item.loan_monthly_payment = 450.00

    # Configure the mock to return a list of these items
    mock_query.all.return_value = [mock_item]

    # Call the endpoint
    response = client.post('/fetchFinance')

    # Check the response
    assert response.status_code == 200
    expected_data = {
        "finances": [
            {"finance_id": 1, "customer_id": 123, "first_name": "John", "last_name": "Doe",
             "car_year": 2020, "car_make": "Toyota", "car_model": "Camry", "car_price": 30000.00,
             "credit_score": 720, "finance_decision": "Approved", "loan_term": 60, "loan_apr": 3.5,
             "monthly_payment": 450.00}
        ]
    }
    assert json.loads(response.data) == expected_data

@patch('server.FinanceContract.query')
def test_fetch_finance_failure(mock_query, client):
    # Configure the mock to raise an exception when all() is called
    mock_query.all.side_effect = Exception("Database error")

    # Call the endpoint
    response = client.post('/fetchFinance')

    # Check the response
    assert response.status_code == 500
    assert json.loads(response.data) == {'error': 'Database error'}




