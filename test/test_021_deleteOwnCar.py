import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json
from server import app, db  # Ensure this import brings in your Flask app or recreate it here if needed

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.db.session.commit')
@patch('server.db.session.delete')
@patch('server.OwnCar.query')
def test_delete_car_success(mock_query, mock_delete, mock_commit, client):
    # Mock the car retrieval
    mock_car = MagicMock()
    mock_query.get.return_value = mock_car

    # Call the endpoint
    response = client.delete('/delete_own_car/123')

    # Check the response
    assert response.status_code == 200
    assert json.loads(response.data) == {'message': 'Car with ID 123 deleted successfully'}

    # Verify that delete and commit were called
    mock_delete.assert_called_with(mock_car)
    mock_commit.assert_called_once()

@patch('server.OwnCar.query')
def test_delete_car_not_found(mock_query, client):
    # Configure the mock to return None when the car is not found
    mock_query.get.return_value = None

    # Call the endpoint
    response = client.delete('/delete_own_car/999')

    # Check the response
    assert response.status_code == 404
    assert json.loads(response.data) == {'error': 'Car with ID 999 not found'}

@patch('server.db.session.commit')
@patch('server.db.session.delete')
@patch('server.OwnCar.query')
def test_delete_car_failure(mock_query, mock_delete, mock_commit, client):
    # Configure the mock to raise an exception
    mock_query.get.side_effect = Exception("Database error")

    # Call the endpoint
    response = client.delete('/delete_own_car/123')

    # Check the response
    assert response.status_code == 500
    assert json.loads(response.data) == {'error': 'Database error'}

    # Verify that commit was not called
    mock_commit.assert_not_called()
