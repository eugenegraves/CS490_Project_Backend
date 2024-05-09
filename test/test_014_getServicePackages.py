import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json, jsonify
from server import app  # Ensure this import brings in your Flask app or recreate it here if needed

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

# Patch the 'ServicesPackage.query' to mock the database query used in your Flask app
@patch('server.ServicesPackage.query')
def test_get_service_package_success(mock_query, client):
    # Setup mock data for services
    mock_service1 = MagicMock()
    mock_service1.service_package_id = 1
    mock_service1.name = 'Basic'
    mock_service1.price = 100.00
    mock_service1.description = 'Basic service package'
    mock_service1.image = 'image1.jpg'

    mock_service2 = MagicMock()
    mock_service2.service_package_id = 2
    mock_service2.name = 'Premium'
    mock_service2.price = 200.00
    mock_service2.description = 'Premium service package'
    mock_service2.image = 'image2.jpg'

    # Configure the mock to return a list of these mocked services when all() is called
    mock_query.all.return_value = [mock_service1, mock_service2]

    # Perform the GET request to the endpoint
    response = client.get('/ServicesPackage')

    # Verify the response status code and data
    assert response.status_code == 200
    expected_data = [
        {
            'service_package_id': 1,
            'name': 'Basic',
            'price': 100.00,
            'description': 'Basic service package',
            'image': 'image1.jpg'
        },
        {
            'service_package_id': 2,
            'name': 'Premium',
            'price': 200.00,
            'description': 'Premium service package',
            'image': 'image2.jpg'
        }
    ]
    # Using json.loads to ensure format and type alignment in comparison
    assert json.loads(response.data) == expected_data

# Optional: Add another test to handle scenarios where no services are found
@patch('server.ServicesPackage.query')
def test_get_service_package_empty(mock_query, client):
    # Configure the mock to return an empty list when all() is called
    mock_query.all.return_value = []

    response = client.get('/ServicesPackage')

    assert response.status_code == 200
    assert json.loads(response.data) == []
