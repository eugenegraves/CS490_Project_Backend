import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from flask import json
from server import app  # Ensure you import your Flask app correctly

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.db.session.commit')
@patch('server.db.session.add')
def test_save_finance_application_success(mock_add, mock_commit, client):
    # Prepare the request data
    request_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'customer_id': 123,
        'email': 'john@example.com',
        'address': '123 Elm St',
        'phone_number': '555-1234',
        'car_year': 2021,
        'car_make': 'Toyota',
        'car_model': 'Camry',
        'car_price': 30000,
        'credit_score': 750,
        'finance_decision': 'Approved',
        'loan_term': 60,
        'down_payment': 5000,
        'loan_apr': 4.5,
        'loan_monthly_payment': 550
    }

    # Call the endpoint with JSON data
    response = client.post('/saveFinanceApplication', json=request_data)

    # Check the response
    assert response.status_code == 201
    assert json.loads(response.data) == {'message': 'Contract/Report Saved Successfully!!'}

    # Verify db interactions
    mock_add.assert_called_once()
    mock_commit.assert_called_once()

@patch('server.db.session.commit')
@patch('server.db.session.add')
def test_save_finance_application_failure(mock_add, mock_commit, client):
    # Prepare the request data with incomplete fields
    request_data = {
        'first_name': 'John',
        'last_name': 'Doe'
        # Missing other required data fields...
    }

    # Set up the mock to raise an exception when commit is attempted
    mock_commit.side_effect = Exception("Database commit error")

    # Call the endpoint with JSON data
    response = client.post('/saveFinanceApplication', json=request_data)

    # Check the response
    assert response.status_code == 500
    assert json.loads(response.data) == {'error': 'Database commit error'}

    # Ensure that commit was attempted but failed
    mock_commit.assert_called_once()
