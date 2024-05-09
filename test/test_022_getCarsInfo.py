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

@patch('server.Cars.query')
def test_get_car_infos_success(mock_query, client):
    # Set up the mock to return your specific test data
    mock_car = MagicMock()
    mock_car.car_id = '123'
    mock_car.make = 'Toyota'
    mock_car.model = 'Camry'
    mock_car.year = 2020
    mock_car.color = 'Red'
    mock_car.engine = '3.5L V6'
    mock_car.transmission = 'Automatic'
    mock_car.price = 30000.00
    mock_car.image0 = 'path/to/image0.jpg'
    mock_car.image1 = 'path/to/image1.jpg'
    mock_car.image2 = 'path/to/image2.jpg'
    mock_car.image3 = 'path/to/image3.jpg'
    mock_car.image4 = 'path/to/image4.jpg'

    mock_query.filter_by.return_value.first.return_value = mock_car

    response = client.get('/getCarInfos?car_id=123')

    assert response.status_code == 200
    expected_data = {
        'car_id': '123',
        'make': 'Toyota',
        'model': 'Camry',
        'year': 2020,
        'color': 'Red',
        'engine': '3.5L V6',
        'transmission': 'Automatic',
        'price': 30000.00,
        'image0': 'path/to/image0.jpg',
        'image1': 'path/to/image1.jpg',
        'image2': 'path/to/image2.jpg',
        'image3': 'path/to/image3.jpg',
        'image4': 'path/to/image4.jpg'
    }
    assert json.loads(response.data) == expected_data

@patch('server.Cars.query')
def test_get_car_infos_not_found(mock_query, client):
    mock_query.filter_by.return_value.first.return_value = None

    response = client.get('/getCarInfos?car_id=999')

    assert response.status_code == 404
    assert json.loads(response.data) == {'error': 'Car not found'}
