import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from flask import json
from server import app, db  # Ensure this import includes your Flask app and SQLAlchemy object

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@patch('server.db.session.commit')
@patch('server.db.session.add')
@patch('server.Cars.query')
@patch('server.Customer.query')
def test_add_car_success(mock_customer_query, mock_cars_query, mock_add, mock_commit, client):
    mock_customer_query.get.return_value = MagicMock(customer_id=1)  # Assume the customer exists
    mock_cars_query.filter_by.return_value.first.return_value = None  # Assume the car ID does not exist

    response = client.post('/add_own_car/1', json={
        'car_id': '123',
        'make': 'Toyota',
        'model': 'Corolla',
        'year': '2020'
    })

    assert response.status_code == 201
    assert json.loads(response.data) == {'message': 'Car added successfully'}

@patch('server.Cars.query')
@patch('server.Customer.query')
def test_add_car_failure_car_exists(mock_customer_query, mock_cars_query, client):
    mock_customer_query.get.return_value = MagicMock(customer_id=1)
    mock_cars_query.filter_by.return_value.first.return_value = MagicMock(car_id='123')  # Car exists

    response = client.post('/add_own_car/1', json={
        'car_id': '123',
        'make': 'Toyota',
        'model': 'Corolla',
        'year': '2020'
    })

    assert response.status_code == 400
    assert json.loads(response.data) == {'error': 'Car ID already exists'}

@patch('server.Cars.query')
@patch('server.Customer.query')
def test_add_car_failure_customer_not_found(mock_customer_query, mock_cars_query, client):
    mock_customer_query.get.return_value = None  # Customer does not exist

    response = client.post('/add_own_car/2', json={
        'car_id': '124',
        'make': 'Honda',
        'model': 'Civic',
        'year': '2019'
    })

    assert response.status_code == 404
    assert json.loads(response.data) == {'error': 'Customer not found'}
