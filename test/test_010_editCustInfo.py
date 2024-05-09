import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
import hashlib
from unittest.mock import patch, MagicMock
from flask import Flask
from server import app  # Make sure this import fetches your Flask app or redefine it here if needed

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.db.session.commit')
@patch('server.Customer.query')
def test_edit_customer(mock_query, mock_commit, client):
    # Create a mock customer object
    mock_customer = MagicMock()
    mock_customer.first_name = 'John'
    mock_customer.last_name = 'Doe'
    mock_customer.email = 'johndoe@example.com'
    mock_customer.phone = '555-0000'
    mock_customer.Address = '101 Main St'
    mock_customer.password = hashlib.sha256('oldpassword'.encode()).hexdigest()
    mock_customer.usernames = 'johndoe'

    # Configure the query mock to return the mock customer when queried by ID
    mock_query.get.return_value = mock_customer

    # Prepare data to be sent to the PUT endpoint
    update_data = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'janedoe@example.com',
        'phone': '555-0101',
        'Address': '123 Elm St',
        'password': 'newpassword123',
        'usernames': 'janedoe'
    }

    # Make the PUT request to update customer data
    response = client.put('/edit-customer/1', json=update_data)

    # Check the updated attributes
    assert mock_customer.first_name == 'Jane'
    assert mock_customer.last_name == 'Doe'
    assert mock_customer.email == 'janedoe@example.com'
    assert mock_customer.phone == '555-0101'
    assert mock_customer.Address == '123 Elm St'
    assert mock_customer.password == hashlib.sha256('newpassword123'.encode()).hexdigest()
    assert mock_customer.usernames == 'janedoe'

    # Ensure the transaction was committed
    mock_commit.assert_called_once()

    # Check response
    assert response.status_code == 200
    assert json.loads(response.data) == {'message': 'User data updated successfully'}

@patch('server.Customer.query')
def test_edit_customer_not_found(mock_query, client):
    # Configure the query mock to return None when a specific customer ID is queried
    mock_query.get.return_value = None

    # Attempt to update a non-existent customer
    response = client.put('/edit-customer/999', json={'first_name': 'Jane'})

    # Check response for non-existing customer
    assert response.status_code == 404
    assert json.loads(response.data) == {'message': 'Customer not found'}
