import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json
from server import app  # Ensure this import brings in your Flask app or recreate it here if needed

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.ItemSold.query')
def test_get_car_sold_success(mock_query, client):
    # Create a list of MagicMock objects to mimic the ItemSold instances returned from the query
    mock_item_sold = MagicMock()
    mock_item_sold.item_sold_id = 1
    mock_item_sold.customer_id = 100
    mock_item_sold.item_type = 'car'
    mock_item_sold.date = MagicMock()
    mock_item_sold.date.strftime.return_value = '2023-05-10 14:00:00'
    mock_item_sold.price = 20000.00
    mock_item_sold.item_id = 10
    mock_item_sold.method_of_payment = 'cash'

    # Configure the mock to return a list containing the mocked item sold when all() is called
    mock_query.filter_by.return_value.all.return_value = [mock_item_sold]

    # Perform the GET request to the endpoint
    response = client.get('/car_sold/100')

    # Verify the response status code and data
    assert response.status_code == 200
    expected_data = [{
        'item_sold_id': 1,
        'customer_id': 100,
        'item_type': 'car',
        'date': '2023-05-10 14:00:00',
        'price': 20000.00,
        'item_id': 10,
        'method_of_payment': 'cash'
    }]
    # Using json.loads to ensure format and type alignment in comparison
    assert json.loads(response.data) == expected_data

@patch('server.ItemSold.query')
def test_get_car_sold_not_found(mock_query, client):
    # Configure the mock to return an empty list when all() is called
    mock_query.filter_by.return_value.all.return_value = []

    # Perform the GET request to the endpoint
    response = client.get('/car_sold/999')

    # Verify the response status code and data
    assert response.status_code == 404
    assert json.loads(response.data) == {'message': 'No items sold found for this customer ID and item type.'}
