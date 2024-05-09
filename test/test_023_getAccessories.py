import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json, jsonify
from sqlalchemy import text
from server import app, db  # Ensure this import includes your Flask app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.db.session.execute')
def test_accessories_success(mock_execute, client):
    """Test successful retrieval of accessories by category."""
    # Mock data returned from the database
    accessories_data = [
        (1, 'Seat Cover', 'High-quality leather seat cover', 99.99, 'image1.jpg'),
        (2, 'Steering Wheel Cover', 'Wooden finish cover', 49.99, 'image2.jpg')
    ]
    mock_result = MagicMock()
    mock_result.fetchall.return_value = accessories_data
    mock_execute.return_value = mock_result

    # Perform the POST request to the endpoint
    response = client.post('/accessories', json={'category': 'Interior'})
    
    # Verify the response status code and data
    assert response.status_code == 200
    expected_data = [
        {'accessoire_id': 1, 'name': 'Seat Cover', 'description': 'High-quality leather seat cover', 'price': 99.99, 'image': 'image1.jpg'},
        {'accessoire_id': 2, 'name': 'Steering Wheel Cover', 'description': 'Wooden finish cover', 'price': 49.99, 'image': 'image2.jpg'}
    ]
    assert json.loads(response.data) == expected_data

@patch('server.db.session.execute')
def test_accessories_failure_exception(mock_execute, client):
    """Test error handling when database throws an exception."""
    mock_execute.side_effect = Exception("Database error")

    # Perform the POST request to the endpoint
    response = client.post('/accessories', json={'category': 'Interior'})

    # Verify the response status code and data
    assert response.status_code == 500
    assert json.loads(response.data) == {'error': 'Database error'}
