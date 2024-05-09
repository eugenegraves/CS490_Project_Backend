import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import jsonify, Flask
from server import app  # Adjust the import according to your actual application structure

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.ServicesOffered.query')
def test_get_all_services(mock_query, client):
    # Setup mock
    mock_service = MagicMock()
    mock_service.services_offered_id = 1
    mock_service.name = 'oil change'
    mock_service.price = 15.00
    mock_service.description = 'Its an oil change'
    mock_service.image = 'image_url.jpg'

    # Configure the mock to return a list containing your mocked service when all() is called
    mock_query.all.return_value = [mock_service]

    # Perform the GET request to the endpoint
    response = client.get('/services-offered')

    # Expected data setup
    expected_data = [{
        'services_offered_id': 1,
        'name': 'oil change',
        'price': 15.00,
        'description': 'Its an oil change',
        'image': 'image_url.jpg'
    }]

    # Verify the response status code and data
    assert response.status_code == 200
    assert response.json == expected_data

@patch('server.ServicesOffered.query')
def test_get_all_services_empty(mock_query, client):
    # Configure the mock to return an empty list when all() is called
    mock_query.all.return_value = []

    # Perform the GET request to the endpoint
    response = client.get('/services-offered')

    # Verify the response status code and data
    assert response.status_code == 200
    assert response.json == []
