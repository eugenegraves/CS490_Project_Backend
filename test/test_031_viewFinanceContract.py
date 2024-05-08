import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json, Flask
from server import app  # Ensure this import brings in your Flask app or recreate it here if needed

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

# Patch the 'FinanceContract.query' where 'FinanceContract' is the import path in your actual application
# @patch('server.FinanceContract.query')
# def test_get_finance_contract(mock_query, client):
#     # Set up the mock to return your specific test data
#     mock_contract = MagicMock()
#     mock_contract.id = 1
#     mock_contract.first_name = 'John'
#     mock_contract.last_name = 'Doe'
#     mock_contract.customer_id = 123
#     mock_contract.email = 'johndoe@email.com'
#     mock_contract.address = '123 Elm Street'
#     mock_contract.phone_number = '555-1234'
#     mock_contract.car_year = 2020
#     mock_contract.car_make = 'Toyota'
#     mock_contract.car_model = 'Camry'
#     mock_contract.car_price = 30000.00
#     mock_contract.credit_score = 720
#     mock_contract.down_payment = 5000.00
#     mock_contract.finance_decision = 'Approved'
#     mock_contract.loan_term = 60
#     mock_contract.loan_apr = 3.5
#     mock_contract.loan_monthly_payment = 450.00

#     # Configure the mock to return a list containing your mocked contract when all() is called
#     mock_query.filter_by.return_value.all.return_value = [mock_contract]

#     # Perform the GET request to the endpoint
#     response = client.get('/view_finance_contract/123')

#     # Verify the response status code and data
#     assert response.status_code == 200
#     expected_data = [{
#         'id': 1,
#         'first_name': 'John',
#         'last_name': 'Doe',
#         'customer_id': 123,
#         'email': 'johndoe@email.com',
#         'address': '123 Elm Street',
#         'phone_number': '555-1234',
#         'car_year': 2020,
#         'car_make': 'Toyota',
#         'car_model': 'Camry',
#         'car_price': 30000.00,
#         'credit_score': 720,
#         'down_payment': 5000.00,
#         'finance_decision': 'Approved',
#         'loan_term': 60,
#         'loan_apr': 3.50,
#         'loan_monthly_payment': 450.00
#     }]
#     # Using json.loads to ensure format and type alignment in comparison
#     assert json.loads(response.data) == expected_data

@patch('server.FinanceContract.query')
def test_get_finance_contract_not_found(mock_query, client):
    mock_query.filter_by.return_value.all.return_value = []

    response = client.get('/view_finance_contract/999')

    assert response.status_code == 404
    assert json.loads(response.data) == {'error': 'Contracts not found'}

