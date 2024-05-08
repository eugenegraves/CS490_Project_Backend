import sys
import os
# Append the directory of server.py to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json
from server import app  # Make sure to import your Flask app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.db.session.commit')
@patch('server.db.session.delete')
@patch('server.Cart.query')
def test_checkout_success(mock_query, mock_delete, mock_commit, client):
    # Mock cart items retrieval
    mock_cart_item = MagicMock()
    mock_query.filter_by.return_value.all.return_value = [mock_cart_item]

    # Call the endpoint
    response = client.delete('/checkout/123')

    # Check the response
    assert response.status_code == 200
    assert json.loads(response.data) == {'mesage': 'successful checkout'}

    # Verify that delete and commit were called
    mock_delete.assert_called_with(mock_cart_item)
    mock_commit.assert_called_once()

@patch('server.db.session.commit')
@patch('server.db.session.delete')
@patch('server.Cart.query')
def test_checkout_failure(mock_query, mock_delete, mock_commit, client):
    # Configure the mock to raise an exception when all() is called
    mock_query.filter_by.return_value.all.side_effect = Exception("Database error")

    # Call the endpoint
    response = client.delete('/checkout/123')

    # Check the response
    assert response.status_code == 500
    assert json.loads(response.data) == {'error': 'Database error'}

    # Verify that commit was not called
    mock_commit.assert_not_called()
