import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json
from server import app  # Ensure this import brings in your Flask app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.db.session.execute')
@patch('server.db.session.commit')
def test_add_accessory_to_cart_success(mock_commit, mock_execute, client):
    # Mock the execute method to simulate the database insert operation
    mock_result = MagicMock()
    mock_result.rowcount = 1  # Simulate one row affected, indicating successful insertion
    mock_execute.return_value = mock_result

    # Define the payload
    payload = {
        "cartData": {
            "customer_id": "123",
            "item_price": "29.99",
            "item_image": "image.jpg",
            "item_name": "Cool Accessory",
            "accessoire_id": "456"
        }
    }

    # Make the POST request
    response = client.post('/addAccessoryToCart', json=payload)

    # Check that the status code is 200
    assert response.status_code == 200
    assert json.loads(response.data) == {'message': 'Accessory added to cart successfully'}
    # Ensure commit was called
    mock_commit.assert_called_once()

@patch('server.db.session.execute')
def test_add_accessory_to_cart_failure_incomplete_data(mock_execute, client):
    # Define the payload with incomplete data
    payload = {
        "cartData": {
            "customer_id": "123",
            "item_image": "image.jpg",
            "item_name": "Cool Accessory"
            # Missing item_price and accessoire_id
        }
    }

    # Make the POST request
    response = client.post('/addAccessoryToCart', json=payload)

    # Check that the status code is 400 for bad request due to incomplete data
    assert response.status_code == 400
    assert json.loads(response.data) == {'error': 'cart data not provided or incomplete'}

@patch('server.db.session.execute')
def test_add_accessory_to_cart_failure_not_json(mock_execute, client):
    # Make the POST request with incorrect data format (not JSON)
    response = client.post('/addAccessoryToCart', data="Not a JSON")

    # Check that the status code is 400 for bad request due to incorrect format
    assert response.status_code == 400
    assert json.loads(response.data) == {'error': 'Request is not in JSON format'}

@patch('server.db.session.execute')
def test_add_accessory_to_cart_exception(mock_execute, client):
    # Simulate a database exception
    mock_execute.side_effect = Exception("Database failure")

    # Define the payload
    payload = {
        "cartData": {
            "customer_id": "123",
            "item_price": "29.99",
            "item_image": "image.jpg",
            "item_name": "Cool Accessory",
            "accessoire_id": "456"
        }
    }

    # Make the POST request
    response = client.post('/addAccessoryToCart', json=payload)

    # Check that the status code is 500 for internal server error
    assert response.status_code == 500
    assert json.loads(response.data) == {'error': 'Failed to add accessory'}

# Ensure patches for db.session.commit and db.session.execute are added to test_add_accessory_to_cart_exception if commit is part of the normal flow
