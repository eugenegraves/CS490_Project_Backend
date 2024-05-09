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

# Mock the function 'fetch_categories_from_database' where it is defined in your actual application
@patch('server.fetch_categories_from_database')
def test_get_categories_success(mock_fetch_categories, client):
    # Set up the mock to return your specific test data
    mock_fetch_categories.return_value = ['Sedan', 'SUV', 'Convertible']

    # Perform the GET request to the endpoint
    response = client.get('/categories')

    # Verify the response status code and data
    assert response.status_code == 200
    expected_data = [
        {'value': 'Sedan', 'label': 'Sedan'},
        {'value': 'SUV', 'label': 'SUV'},
        {'value': 'Convertible', 'label': 'Convertible'}
    ]
    # Using json.loads to ensure format and type alignment in comparison
    assert json.loads(response.data) == expected_data

@patch('server.fetch_categories_from_database')
def test_get_categories_empty(mock_fetch_categories, client):
    # Configure the mock to return an empty list
    mock_fetch_categories.return_value = []

    # Perform the GET request to the endpoint
    response = client.get('/categories')

    # Verify the response status code and data
    assert response.status_code == 200
    assert json.loads(response.data) == []
