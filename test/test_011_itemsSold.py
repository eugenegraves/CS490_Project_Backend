import sys
import os
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

@patch('server.ItemSold.query')
def test_get_items_sold(mock_query, client):
    # Mock data setup
    mock_item1 = MagicMock()
    mock_item1.item_sold_id = 1
    mock_item1.customer_id = 101
    mock_item1.item_type = 'cover'
    mock_item1.date = MagicMock(isoformat=lambda: '2022-05-15T12:34:56')
    mock_item1.price = 29.99
    mock_item1.item_id = 201
    mock_item1.method_of_payment = 'Credit Card'

    mock_item2 = MagicMock()
    mock_item2.item_sold_id = 2
    mock_item2.customer_id = 101
    mock_item2.item_type = 'case'
    mock_item2.date = MagicMock(isoformat=lambda: '2022-05-16T14:30:00')
    mock_item2.price = 59.99
    mock_item2.item_id = 202
    mock_item2.method_of_payment = 'Debit Card'

    # Configure the mock to return a list containing your mocked items when all() is called
    mock_query.filter_by.return_value.all.return_value = [mock_item1, mock_item2]

    # Perform the GET request to the endpoint
    response = client.get('/items-sold/101')

    # Verify the response status code and data
    assert response.status_code == 200
    expected_data = [
        {
            'item_sold_id': 1,
            'customer_id': 101,
            'item_type': 'cover',
            'date': '2022-05-15T12:34:56',
            'price': 29.99,
            'item_id': 201,
            'method_of_payment': 'Credit Card'
        },
        {
            'item_sold_id': 2,
            'customer_id': 101,
            'item_type': 'case',
            'date': '2022-05-16T14:30:00',
            'price': 59.99,
            'item_id': 202,
            'method_of_payment': 'Debit Card'
        }
    ]
    # Using json.loads to ensure format and type alignment in comparison
    assert json.loads(response.data) == expected_data

@patch('server.ItemSold.query')
def test_get_items_sold_not_found(mock_query, client):
    # Configure the mock to return an empty list when no items are found
    mock_query.filter_by.return_value.all.return_value = []

    # Perform the GET request to the endpoint
    response = client.get('/items-sold/999')

    # Verify the response status code and data
    assert response.status_code == 404
    assert json.loads(response.data) == {'message': 'No items found for the given customer ID'}
