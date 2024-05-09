import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json
from server import app, db  # Ensure these imports are correctly resolving to your Flask app and database setup

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.db.session.add')
@patch('server.db.session.commit')
def test_add_cars_to_site_success(mock_commit, mock_add, client):
    # Prepare the data to send with the request
    car_data = {
        "cars": [
            {
                "manager_id": 1,
                "make": "Toyota",
                "model": "Camry",
                "year": 2020,
                "color": "red",
                "engine": "2.5L",
                "transmission": "Automatic",
                "price": 22000.00,
                "image0": "image0.jpg",
                "image1": "image1.jpg",
                "image2": "image2.jpg",
                "image3": "image3.jpg",
                "image4": "image4.jpg"
            }
        ]
    }

    # Perform the POST request to the endpoint
    response = client.post('/add_cars_to_site', json=car_data)

    # Check that the response status code and message are correct
    assert response.status_code == 201
    assert json.loads(response.data) == {'message': 'Cars added successfully to the dealership'}

    # Verify that add and commit were called
    assert mock_add.called
    mock_commit.assert_called_once()

@patch('server.db.session.add')
@patch('server.db.session.commit')
def test_add_cars_to_site_failure(mock_commit, mock_add, client):
    # Test case with missing car data fields to see handling of incomplete data
    car_data = {
        "cars": [
            {
                "manager_id": 1,
                "make": "Toyota"
                # Missing many required fields
            }
        ]
    }

    # Attempt to add incomplete data
    response = client.post('/add_cars_to_site', json=car_data)

    # We expect a failure due to incomplete data; check if 400 or a specific error is handled
    # This assertion depends on how your actual endpoint handles errors.
    # Here we assume a generic 400 response for simplification.
    assert response.status_code == 400  # Adjust according to your endpoint's error handling

    # Ensure no commit occurs due to the error
    mock_commit.assert_not_called()
